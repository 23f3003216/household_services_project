import ServiceResource from "../components/ServiceResource.js";

const CustomerDashboard = {
  template: `
  <div>
    <h1 class="text-center">Customer Dashboard</h1>
    
    <!-- Search Functionality -->
    <div class="search-bar mb-3">
      <label for="searchType">Search by:</label>
      <select v-model="searchType" id="searchType" class="form-control d-inline w-auto">
        <option value="service_name">Service Name</option>
      </select>
      <input type="text" v-model="searchText" placeholder="Enter search text" class="form-control d-inline w-auto" />
      <button @click="performSearch" class="btn btn-primary">Search</button>
    </div>
    
    <button @click="fetchServiceHistory" class="btn btn-info mb-3">View Service History</button>
    
    <div v-if="serviceHistory.length">
      <h2>Service History</h2>
      <div class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Service Name</th>
              <th>Professional Name</th>
              <th>Phone</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="history in serviceHistory" :key="history.id">
              <td>{{ history.id }}</td>
              <td>{{ history.service_name }}</td>
              <td>{{ history.professional_name }}</td>
              <td>{{ history.phone }}</td>
              <td>{{ history.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div v-if="selectedService">
      <h2>Professionals for {{ selectedService.name }}</h2>
      <div class="d-flex flex-row p-5" v-for="professional in servicePackages" :key="professional.id">
        <ServiceResource 
          :name="professional.name" 
          :price="professional.price" 
          :description="professional.description" 
          :time_required="professional.time_required"
          :experience="professional.experience"  
          :phone="professional.phone"  
          :address="professional.address" 
          @bookService="bookService(professional)"
        />
      </div>
      <button @click="clearSelection">Back to Services</button>
    </div>
    
    <div v-else>
      <div class="d-flex flex-row p-5" v-for="service in filteredServices" :key="service.id" @click="fetchServicePackages(service)">
        <ServiceResource 
          :name="service.name" 
          :price="service.price" 
          :description="service.description" 
          :time_required="service.time_required"
        />
      </div>
    </div>
  </div>
`,
  components: {
    ServiceResource,
  },
  data() {
    return {
      allServices: [],
      filteredServices: [],
      selectedService: null, 
      servicePackages: [],
      serviceHistory: [],
      searchText: '',
      searchType: 'service_name',
    };
  },
  mounted() {
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await fetch("/api/services"); 
        const data = await response.json();
        this.allServices = data;
        this.filteredServices = data; 
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    performSearch() {
      if (this.searchText) {
        this.filteredServices = this.allServices.filter(service => {
          return service.name.toLowerCase().includes(this.searchText.toLowerCase());
        });
      } else {
        this.filteredServices = this.allServices; // Reset to all services if search text is empty
      }
    },
    async fetchServicePackages(service) {
      try {
        this.selectedService = service;
        const response = await fetch(`/api/service-packages/${service.id}`); 
        const data = await response.json();
        this.servicePackages = data;
      } catch (error) {
        console.error("Error fetching service packages:", error);
      }
    },
    async bookService(professional) {
      try {
        const response = await fetch("/api/service-requests", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            service_id: this.selectedService.id,
            professional_id: professional.id,
          }),
        });
        const data = await response.json();
        alert(data.message || "Service requested successfully");
      } catch (error) {
        console.error("Error booking service:", error);
      }
    },
    async fetchServiceHistory() {
      try {
        const response = await fetch("/api/service-history"); 
        const data = await response.json();
        this.serviceHistory = data.service_history; 
      } catch (error) {
        console.error("Error fetching service history:", error);
      }
    },
    clearSelection() {
      this.selectedService = null;
      this.servicePackages = [];
    },
  },
};

export default CustomerDashboard;
