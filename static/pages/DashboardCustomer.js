import ServiceResource from "../components/ServiceResource.js";

const CustomerDashboard = {
  template: `
  <div>
    <h1 class="text-center">Customer Dashboard</h1>
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
          :pincode="professional.pincode" 
          @bookService="bookService(professional)"
        />
      </div>
      <button @click="clearSelection">Back to Services</button>
    </div>
    <div v-else>
      <div class="d-flex flex-row p-5" v-for="service in allServices" :key="service.id" @click="fetchServicePackages(service)">
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
    clearSelection() {
      this.selectedService = null;
      this.servicePackages = [];
    },
  },
};

export default CustomerDashboard;
