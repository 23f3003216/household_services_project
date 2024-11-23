import router from "../utils/router.js";

const Login = {
  template: `
    <div class="d-flex justify-content-center align-items-center vh-100">
      <div class="card shadow p-4 border rounded-3 ">
        <h3 class="card-title text-center mb-4">Login</h3>
        <div class="form-group mb-3">
          <input v-model="email" type="email" class="form-control" placeholder="Email" required/>
        </div>
        <div class="form-group mb-4">
          <input v-model="password" type="password" class="form-control" placeholder="Password" required/>
        </div>
        <button class="btn btn-primary w-100" @click="submitInfo">Login</button>
      </div>
    </div>
  `,
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async submitInfo() {
      const origin = window.location.origin;
      const url = `${origin}/user-login`;
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: this.email, password: this.password }),
        credentials: "same-origin",
      });

      if (res.ok) {
        const data = await res.json();
        console.log(data);

        // Check the user role and handle the response accordingly
        if (data.role === 'customer') {
          router.push("/customer-dashboard");
        } else if (data.role === 'service_professional') {
          if (data.professional_id) {
            localStorage.setItem('professional_id', data.professional_id);
          }

          router.push("/service-dashboard");
        } else if (data.role === 'admin') {
          router.push("/admin-dashboard");
        } else {
          console.error("Unknown role:", data.role);
        }
      } else {
        const errorData = await res.json();
        console.error("Login failed:", errorData);
      }
    },
  },
};

export default Login;
