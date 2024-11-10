import ServiceResource from "../components/ServiceResource.js";

const DashboardServiceProfessional = {
  template: `
  <div>
    <h1 class="text-center">Professional Dashboard</h1>
    
    <button @click="fetchServiceRequests" class="btn btn-info mb-3">View Service Requests</button>
    
    <div v-if="serviceRequests.length">
      <h2>Service Requests</h2>
      <div class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th>Service Name</th>
              <th>Customer Name</th>
              <th>Phone</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in serviceRequests" :key="request.id">
              <td>{{ request.service_name }}</td>
              <td>{{ request.customer_name }}</td>
              <td>{{ request.phone }}</td>
              <td>{{ request.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="selectedRequest">
      <h2>Service Request Details</h2>
      <div class="d-flex flex-row p-5">
        <ServiceResource 
          :name="selectedRequest.service_name" 
          :price="selectedRequest.price" 
          :description="selectedRequest.description" 
          :time_required="selectedRequest.time_required"
          :experience="selectedRequest.experience"
          :phone="selectedRequest.phone"
          :address="selectedRequest.address"
        />
      </div>
      <button @click="clearSelection">Back to Service Requests</button>
    </div>
  </div>
  `,
  components: {
    ServiceResource,
  },
  data() {
    return {
      serviceRequests: [],  // Stores all service requests for the professional
      selectedRequest: null,  // Stores the selected request for detailed view
    };
  },
  mounted() {
    this.fetchServiceRequests();  // Fetch all service requests when the component is mounted
  },
  methods: {
    // Fetch service requests for the professional using the professional ID from localStorage
    async fetchServiceRequests() {
      try {
        // Retrieve the professional ID from localStorage (this key should match the one used in Login)
        const professionalId = localStorage.getItem('professional_id');  // Adjust the key as necessary

        if (!professionalId) {
          console.error('Professional ID not found in login data');
          return;
        }

        // Fetch service requests by professionalId from the backend
        const response = await fetch(`/api/service-requests/professional/${professionalId}`);
        if (response.ok) {
          const data = await response.json();
          this.serviceRequests = data;  // Store the fetched service requests in the component's data
        } else {
          console.error('Error fetching service requests');
        }
      } catch (error) {
        console.error('Error fetching service requests:', error);
      }
    },

    // Handle selecting a service request to view details
    clearSelection() {
      this.selectedRequest = null;  // Clear the selected request to return to the list view
    },
  },
};

export default DashboardServiceProfessional;
