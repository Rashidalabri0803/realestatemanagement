from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .forms import (
    BuildingForm,
    ExpenseForm,
    LeaseContractForm,
    MaintenanceRequestForm,
    UnitForm,
)
from .models import (
    Building,
    Expense,
    LeaseContract,
    MaintenanceRequest,
    Unit,
)
from .serializers import (
    BuildingSerializer,
    ExpenseSerializer,
    LeaseContractSerializer,
    MaintenanceRequestSerializer,
    UnitSerializer,
)


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.prefetch_related('total_units').all()
    serializer_class = BuildingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'address']
    search_fields = ['name', 'address']
    ordering_fields = ['created_at', 'updated_at']

    @action(detail=True, methods=['get'])
    def units(self, request, pk=None):
        building = get_object_or_404(Building, pk=pk)
        units = building.total_units.all()
        serializer = UnitSerializer(units, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total_buildings = Building.objects.count()
        total_units = Unit.objects.count()
        rented_units = Unit.objects.filter(status='rented').count()
        available_units = Unit.objects.filter(status='available').count()
        return Response({
            'total_buildings': total_buildings,
            'total_units': total_units,
            'rented_units': rented_units,
            'available_units': available_units,
        })

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.select_related('building').all()
    serializer_class = UnitSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['building', 'unit_type', 'status']
    search_fields = ['number', 'building__name']
    ordering_fields = ['monthly_rent', 'area' , 'created_at']

    @action(detail=False, methods=['get'])
    def available_units(self, request):
        available_units = Unit.objects.filter(status='available')
        serializer = self.get_serializer(available_units, many=True, context={'request': request})
        return Response(serializer.data)

class LeaseContractViewSet(viewsets.ModelViewSet):
    queryset = LeaseContract.objects.select_related('unit', 'tenant').all()
    serializer_class = LeaseContractSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['unit', 'tenant', 'is_active']
    search_fields = ['unit__number', 'tenant__full_name']
    ordering_fields = ['start_date', 'end_date']

    @action(detail=False, methods=['get'])
    def expired_contracts(self, request):
        expired_contracts = LeaseContract.objects.filter(end_date__lt=now(), is_active=True)
        serializer = self.get_serializer(expired_contracts, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def terminate_contract(self, request):
        contract_id = request.data.get('contract_id')
        contract = get_object_or_404(LeaseContract, pk=contract_id)
        contract.is_active = False
        contract.save()
        return Response({'message': f'تم إنهاء عقد الإيجار {contract_id} بنجاح.'}, status=status.HTTP_200_OK)

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.select_related('unit').all()
    serializer_class = MaintenanceRequestSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['unit', 'is_resolved']
    ordering_fields = ['request_date', 'resolved_date']

    @action(detail=False, methods=['get'])
    def unresolved(self, request):
        unresolved_requests = MaintenanceRequest.objects.filter(is_resolved=False)
        serializer = self.get_serializer(unresolved_requests, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def bulk_resolve(self, request):
        request_ids = request.data.get('request_ids', [])
        MaintenanceRequest.objects.filter(id__in=request_ids).update(is_resolved=True)
        return Response({'message': f'تم معالجة {len(request_ids)} طلب صيانة'}, status=status.HTTP_200_OK)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.select_related('building').all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['building', 'date']
    ordering_fields = ['amount', 'date']
        
class BuildingListView(ListView):
    model = Building
    template_name = 'buildings/list.html'
    context_object_name = 'buildings'

class BuildingDetailView(DetailView):
    model = Building
    template_name = 'buildings/detail.html'
    context_object_name = 'building'

class BuildingCreateView(CreateView):
    model = Building
    template_name = 'buildings/form.html'
    form_class = BuildingForm
    success_url = reverse_lazy('list')

class BuildingUpdateView(UpdateView):
    model = Building
    template_name = 'buildings/form.html'
    form_class = BuildingForm
    success_url = reverse_lazy('list')

class BuildingDeleteView(DeleteView):
    model = Building
    template_name = 'rental_management/building_confirm_delete.html'
    success_url = reverse_lazy('list')

class UnitListView(ListView):
    model = Unit
    template_name = 'units/list.html'
    context_object_name = 'units'

class UnitCreateView(CreateView):
    model = Unit
    template_name = 'units/form.html'
    form_class = UnitForm
    success_url = reverse_lazy('list')

class UnitUpdateView(UpdateView):
    model = Unit
    template_name = 'units/form.html'
    form_class = UnitForm
    success_url = reverse_lazy('list')

class UnitDeleteView(DeleteView):
    model = Unit
    template_name = 'rental_management/unit_confirm_delete.html'
    success_url = reverse_lazy('list')


class LeaseContractListView(ListView):
    model = LeaseContract
    template_name = 'lease_contracts/list.html'
    context_object_name = 'contracts'

class LeaseContractCreateView(CreateView):
    model = LeaseContract
    template_name = 'lease_contracts/form.html'
    form_class = LeaseContractForm
    success_url = reverse_lazy('list')

class LeaseContractUpdateView(UpdateView):
    model = LeaseContract
    template_name = 'lease_contracts/form.html'
    form_class = LeaseContractForm
    success_url = reverse_lazy('list')

class LeaseContractDeleteView(DeleteView):
    model = LeaseContract
    template_name = 'rental_management/lease_contract_confirm_delete.html'
    success_url = reverse_lazy('list')

class MaitenanceRequestListView(ListView):
    model = MaintenanceRequest
    template_name = 'maintenance_requests/list.html'
    context_object_name = 'maintenance_requests'

class MaitenanceRequestCreateView(CreateView):
    model = MaintenanceRequest
    template_name = 'maintenance_requests/form.html'
    form_class = MaintenanceRequestForm
    success_url = reverse_lazy('list')

class MaitenanceRequestUpdateView(UpdateView):
    model = MaintenanceRequest
    template_name = 'rental_management/form.html'
    form_class = MaintenanceRequestForm
    success_url = reverse_lazy('list')

class MaitenanceRequestDeleteView(DeleteView):
    model = MaintenanceRequest
    template_name = 'rental_management/maintenance_request_confirm_delete.html'
    success_url = reverse_lazy('list')

class ExpenseListView(ListView):
    model = Expense
    template_name = 'rental_management/expense_list.html'
    context_object_name = 'expenses'

class ExpenseCreateView(CreateView):
    model = Expense
    template_name = 'rental_management/expense_form.html'
    form_class = ExpenseForm
    success_url = reverse_lazy('expense_list')

class ExpenseUpdateView(UpdateView):
    model = Expense
    template_name = 'rental_management/expense_form.html'
    form_class = ExpenseForm
    success_url = reverse_lazy('expense_list')

class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = 'rental_management/expense_confirm_delete.html'
    success_url = reverse_lazy('expense_list')