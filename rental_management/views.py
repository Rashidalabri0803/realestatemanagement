from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
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
from django.db.models import Sum
from django.utils.timezone import now
from .forms import (
    BuildingForm,
    ExpenseForm,
    LeaseContractForm,
    MaintenanceRequestForm,
    TenantForm,
    UnitForm,
)
from .models import (
    Attachment,
    Building,
    Expense,
    LeaseContract,
    MaintenanceRequest,
    Notifiction,
    Payment,
    Tenant,
    Unit,
)
from .serializers import (
    AttachmentSerializer,
    BuildingSerializer,
    ExpenseSerializer,
    LeaseContractSerializer,
    MaintenanceRequestSerializer,
    NotifictionSerializer,
    PaymentSerializer,
    TenantSerializer,
    UnitSerializer,
)


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.prefetch_related('unit_set').all()
    serializer_class = BuildingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'address']
    search_fields = ['name', 'address']
    ordering_fields = ['created_at', 'updated_at']

    @action(detail=True, methods=['get'])
    def units(self, request, pk=None):
        building = get_object_or_404(Building, pk=pk)
        units = building.unit_set.all()
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

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['full_name', 'phone_number', 'email']
    ordering_fields = ['full_name']

    @action(detail=True, methods=['get'])
    def contracts(self, request, pk=None):
        tenant = get_object_or_404(Tenant, pk=pk)
        contracts = LeaseContract.objects.filter(tenant=tenant)
        serializer = LeaseContractSerializer(contracts, many=True, context={'request': request})
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

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('contract').all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['contract', 'payment_date']
    ordering_fields = ['payment_date' , 'amount']

    @action(detail=False, methods=['get'])
    def payment_statistics(self, request):
        total_payments = Payment.objects.all().aggregate(total_amount=models.Sum('amount'))['total'] or 0
        latest_payment = Payment.objects.latest('payment_date') if Payment.objects.all().exists() else None
        latest_payment_data = {
            'amount': latest_payment.amount,
            'payment_date': latest_payment.payment_date,
            'contract': latest_payment.contract.id,
        } if latest_payment else None
        return Response({
            'total_payments': total_payments,
            'latest_payment': latest_payment_data,
        })

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

class NotifictionViewSet(viewsets.ModelViewSet):
    queryset = Notifiction.objects.all()
    serializer_class = NotifictionSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']

    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        Notifiction.objects.update(is_read=True)
        return Response({'message': 'تم تحديد جميع الإشعارات كمقروءة .'}, status=status.HTTP_200_OK)

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.select_related('contract').all()
    serializer_class = AttachmentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ['contract__id', 'description']
    ordering_fields = ['contract', 'id']
        
class BuildingListView(ListView):
    model = Building
    template_name = 'rental_management/building_list.html'
    context_object_name = 'buildings'

class BuildingDetailView(DetailView):
    model = Building
    template_name = 'rental_management/building_detail.html'
    context_object_name = 'building'

class BuildingCreateView(CreateView):
    model = Building
    template_name = 'rental_management/building_form.html'
    form_class = BuildingForm
    success_url = reverse_lazy('building_list')

class BuildingUpdateView(UpdateView):
    model = Building
    template_name = 'rental_management/building_form.html'
    form_class = BuildingForm
    success_url = reverse_lazy('building_list')

class BuildingDeleteView(DeleteView):
    model = Building
    template_name = 'rental_management/building_confirm_delete.html'
    success_url = reverse_lazy('building_list')

class UnitListView(ListView):
    model = Unit
    template_name = 'rental_management/unit_list.html'
    context_object_name = 'units'

class UnitCreateView(CreateView):
    model = Unit
    template_name = 'rental_management/unit_form.html'
    form_class = UnitForm
    success_url = reverse_lazy('unit_list')

class UnitUpdateView(UpdateView):
    model = Unit
    template_name = 'rental_management/unit_form.html'
    form_class = UnitForm
    success_url = reverse_lazy('unit_list')

class UnitDeleteView(DeleteView):
    model = Unit
    template_name = 'rental_management/unit_confirm_delete.html'
    success_url = reverse_lazy('unit_list')

class TenantListView(ListView):
    model = Tenant
    template_name = 'rental_management/tenant_list.html'
    context_object_name = 'tenants'

class TenantCreateView(CreateView):
    model = Tenant
    template_name = 'rental_management/tenant_form.html'
    form_class = TenantForm
    success_url = reverse_lazy('tenant_list')

class TenantUpdateView(UpdateView):
    model = Tenant
    template_name = 'rental_management/tenant_form.html'
    form_class = TenantForm
    success_url = reverse_lazy('tenant_list')

class TenantDeleteView(DeleteView):
    model = Tenant
    template_name = 'rental_management/tenant_confirm_delete.html'
    success_url = reverse_lazy('tenant_list')

class LeaseContractListView(ListView):
    model = LeaseContract
    template_name = 'rental_management/lease_contract_list.html'
    context_object_name = 'contracts'

class LeaseContractCreateView(CreateView):
    model = LeaseContract
    template_name = 'rental_management/lease_contract_form.html'
    form_class = LeaseContractForm
    success_url = reverse_lazy('lease_contract_list')

class LeaseContractUpdateView(UpdateView):
    model = LeaseContract
    template_name = 'rental_management/lease_contract_form.html'
    form_class = LeaseContractForm
    success_url = reverse_lazy('lease_contract_list')

class LeaseContractDeleteView(DeleteView):
    model = LeaseContract
    template_name = 'rental_management/lease_contract_confirm_delete.html'
    success_url = reverse_lazy('lease_contract_list')

class MaitenanceRequestListView(ListView):
    model = MaintenanceRequest
    template_name = 'rental_management/maintenance_request_list.html'
    context_object_name = 'maintenance_requests'

class MaitenanceRequestCreateView(CreateView):
    model = MaintenanceRequest
    template_name = 'rental_management/maintenance_request_form.html'
    form_class = MaintenanceRequestForm
    success_url = reverse_lazy('maintenance_request_list')

class MaitenanceRequestUpdateView(UpdateView):
    model = MaintenanceRequest
    template_name = 'rental_management/maintenance_request_form.html'
    form_class = MaintenanceRequestForm
    success_url = reverse_lazy('maintenance_request_list')

class MaitenanceRequestDeleteView(DeleteView):
    model = MaintenanceRequest
    template_name = 'rental_management/maintenance_request_confirm_delete.html'
    success_url = reverse_lazy('maintenance_request_list')

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

class NotifictionListView(ListView):
    model = Notifiction
    template_name = 'rental_management/notifiction_list.html'
    context_object_name = 'notifictions'