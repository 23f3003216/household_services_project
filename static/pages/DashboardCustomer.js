import ServiceResource from "../components/ServiceResource.js";

const CustomerDashboard = {
  template: `
    <div>
      <h1 class="text-center">Customer Dashboard</h1>
      <div class="d-flex flex-row p-5" v-for="service in allServices" :key="service.id">
        <ServiceResource 
          :name="service.name" 
          :price="service.price" 
          :description="service.description" 
          :time_required="service.time_required"
        />
      </div>
    </div>
  `,
  components: {
    ServiceResource,
  },
  data() {
    return {
      allServices: [],
      selectedService: null, 
      servicePackages: [],
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
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    async fetchServicePackages(service) {
      try {
        this.selectedService = service;
        const response = await fetch(`/api/service-packages/${service.id}`); // Fetching packages for the selected service
        const data = await response.json();
        this.servicePackages = data;
      } catch (error) {
        console.error("Error fetching service packages:", error);
      }
    },
    clearSelection() {
      this.selectedService = null;
      this.servicePackages = [];
    },
  },
};

export default CustomerDashboard;
