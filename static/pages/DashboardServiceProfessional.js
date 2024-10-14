import ServiceRequest from "../components/ServiceRequest.js"; 

const DashboardServiceProfessional = {
  template: `
    <div>
      <h1>Service Professional Dashboard</h1>
      <p>Manage your services, view requests, and track bookings.</p>
      
      <h2>Today's Service Requests</h2>
      <div v-if="serviceRequests.length === 0">No service requests for today.</div>
      <div v-for="request in serviceRequests" :key="request.id">
        <ServiceRequest 
          :customerName="request.customer.name" 
          :contactPhone="request.customer.phone" 
          :location="request.customer.address" 
          :pincode="request.customer.pincode" 
          :requestId="request.id" 
          @accept="acceptRequest" 
          @reject="rejectRequest"
        />
      </div>
    </div>
  `,
  data() {
    return {
      serviceRequests: [],
    };
  },
  async mounted() {
    await this.fetchServiceRequests();
  },
  methods: {
    async fetchServiceRequests() {
      const res = await fetch(`${window.location.origin}/api/service-requests`);
      if (res.ok) {
        const requests = await res.json();
        // Filter requests for today's date or any specific condition as per your needs
        this.serviceRequests = requests.filter(request => request.date_of_request === new Date().toISOString().split('T')[0]);
      }
    },
    async acceptRequest(requestId) {
      // Logic to accept the request
      const res = await fetch(`${window.location.origin}/api/service-requests/${requestId}/accept`, { method: 'POST' });
      if (res.ok) {
        await this.fetchServiceRequests(); // Refresh the requests
      }
    },
    async rejectRequest(requestId) {
      // Logic to reject the request
      const res = await fetch(`${window.location.origin}/api/service-requests/${requestId}/reject`, { method: 'POST' });
      if (res.ok) {
        await this.fetchServiceRequests(); // Refresh the requests
      }
    }
  },
};

export default DashboardServiceProfessional;
