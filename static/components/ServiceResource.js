const ServiceResource = {
    template: `
      <div>
        <div class="card shadow-sm p-4 mb-4 service-card" @click="openPopup">
          <div class="card-body">
            <h3 class="card-title text-center mb-3 text-primary text-truncate">{{ name }}</h3>
            <p class="card-text text-secondary text-truncate">Price: ₹{{ price }}</p>
            <p class="card-text text-secondary text-truncate">Time Required: {{ time_required }} mins</p>
          </div>
        </div>
        <div v-if="showPopup" class="popup-overlay d-flex align-items-center justify-content-center">
          <div class="popup-content card shadow p-4">
            <h3 class="card-title text-center mb-3 text-primary">{{ name }}</h3>
            <p class="card-text text-secondary">Price: ₹{{ price }}</p>
            <p class="card-text text-secondary">Time Required: {{ time_required }} mins</p>
            <p class="card-text">{{ description }}</p>
            <button class="btn btn-secondary mt-3" @click="closePopup">Close</button>
          </div>
        </div>
      </div>
    `,
    props: {
      name: {
        type: String,
        required: true,
      },
      price: {
        type: Number,
        required: true,
      },
      description: {
        type: String,
        required: true,
      },
      time_required: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        showPopup: false, // Controls whether the popup is visible
      };
    },
    methods: {
      openPopup() {
        this.showPopup = true;
      },
      closePopup() {
        this.showPopup = false;
      },
    },
    mounted() {
      const style = document.createElement("style");
      style.textContent = `
        .service-card {
          max-width: 600px;
          margin: auto;
          border-radius: 15px;
          transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }
        .service-card:hover {
          transform: scale(1.02);
          box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
      `;
      document.head.appendChild(style);
    },
  };
  
  export default ServiceResource;
  