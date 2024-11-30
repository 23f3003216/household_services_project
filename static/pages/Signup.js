const Signup = {
  template: `
    <div class="d-flex justify-content-center align-items-center vh-100">
      <div class="card shadow p-4">
        <h3 class="card-title text-center mb-4">Sign Up</h3>

        <div v-if="message" class="alert" :class="{'alert-success': success, 'alert-danger': !success}" role="alert">
          {{ message }}
        </div>

        <div class="form-group mb-3">
          <input v-model="email" type="email" class="form-control" placeholder="Email" required/>
        </div>
        <div class="form-group mb-4">
          <input v-model="password" type="password" class="form-control" placeholder="Password" required/>
        </div>
        <div class="form-group mb-4">
          <select v-model="role" class="form-control" @change="toggleRoleFields">
            <option value="customer">Customer</option>
            <option value="service_professional">Service Professional</option>
          </select>
        </div>
        
        <div class="form-group mb-3" v-if="showCommonFields">
          <input v-model="name" type="text" class="form-control" placeholder="Full Name" required/>
          <input v-model="address" type="text" class="form-control" placeholder="Address" required/>
          <input v-model="phone" type="text" class="form-control" placeholder="Phone" required/>
          <input v-model="pincode" type="text" class="form-control" placeholder="Pincode" required/>
        </div>

        <!-- Service Professional Fields -->
        <div v-if="role === 'service_professional'">
          <div class="form-group mb-3">
            <select v-model="serviceType" class="form-control" required>
              <option disabled value="">Select Service Type</option>
              <option>Plumbing</option>
              <option>AC Servicing</option>
              <option>Electrician</option>
            </select>
          </div>
          <div class="form-group mb-3">
            <input v-model="experience" type="number" class="form-control" placeholder="Experience (in years)" required/>
          </div>
          <div class="form-group mb-3">
            <input type="file" @change="handleFileUpload" class="form-control" required/>
          </div>
        </div>

        <button class="btn btn-primary w-100" @click="submitInfo">Sign Up</button>
      </div>
    </div>
  `,
  data() {
    return {
      email: "",
      password: "",
      role: "customer",
      name: "",
      address: "",
      phone: "",
      pincode: "",
      serviceType: "",
      experience: 0,
      file: null,
      showCommonFields: true,
      message: "",
      success: false,
    };
  },
  methods: {
    toggleRoleFields() {
      this.showCommonFields = true;
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async submitInfo() {
      const formData = new FormData();
      formData.append("email", this.email);
      formData.append("password", this.password);
      formData.append("role", this.role);
      formData.append("name", this.name);
      formData.append("address", this.address);
      formData.append("phone", this.phone);
      formData.append("pincode", this.pincode);

      if (this.role === 'service_professional') {
        formData.append("service_type", this.serviceType);
        formData.append("experience", this.experience);
        formData.append("documents", this.file); 
      }

      const origin = window.location.origin;
      const url = `${origin}/register`;
      const res = await fetch(url, {
        method: "POST",
        body: formData,  
        credentials: "same-origin",
      });

      if (res.ok) {
        const data = await res.json();
        this.message = "Account created successfully!";
        this.success = true;
        setTimeout(() => {
          router.push("/login");
        }, 2000); 
      } else {
        const errorData = await res.json();
        this.message = "Sign up failed: " + errorData.message;
        this.success = false;
        console.error("Sign up failed:", errorData);
      }
    },
  },
};
export default Signup;
