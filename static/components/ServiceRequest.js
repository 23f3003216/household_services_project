// ServiceRequest.js
const ServiceRequest = {
    template: `
      <div class="service-request">
        <p><strong>Customer Name:</strong> {{ customerName }}</p>
        <p><strong>Contact Phone:</strong> {{ contactPhone }}</p>
        <p><strong>Location:</strong> {{ location }}</p>
        <p><strong>Pincode:</strong> {{ pincode }}</p>
        <button class="btn btn-success" @click="accept">Accept</button>
        <button class="btn btn-danger" @click="reject">Reject</button>
      </div>
    `,
    props: {
      customerName: {
        type: String,
        required: true,
      },
      contactPhone: {
        type: String,
        required: true,
      },
      location: {
        type: String,
        required: true,
      },
      pincode: {
        type: Number,
        required: true,
      },
      requestId: {
        type: Number,
        required: true,
      },
    },
    methods: {
      accept() {
        this.$emit('accept', this.requestId);
      },
      reject() {
        this.$emit('reject', this.requestId);
      },
    },
    mounted() {
      const style = document.createElement("style");
      style.textContent = `
        .service-request {
          border: 1px solid #ccc;
          padding: 10px;
          margin: 10px 0;
          border-radius: 10px;
          transition: box-shadow 0.2s ease-in-out;
        }
        .service-request:hover {
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
      `;
      document.head.appendChild(style);
    },
  };
  
  export default ServiceRequest;
  