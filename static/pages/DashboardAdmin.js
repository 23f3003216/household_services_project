import router from "../utils/router.js";

const AdminDashboard = {
  template: `
  <div>
    <h1 class="text-center">Admin Dashboard</h1>

    <!-- Search Functionality -->
    <div class="search-bar mb-3">
      <label for="searchField">Search by:</label>
      <select v-model="searchField" id="searchField" class="form-control d-inline w-auto">
        <option value="email">Email</option>
        <option value="role">Role</option>
      </select>
      <input type="text" v-model="searchText" placeholder="Enter search text" class="form-control d-inline w-auto" />
      <button @click="filterUsers" class="btn btn-primary">Search</button>
      <button @click="resetFilters" class="btn btn-secondary">Reset</button>
    </div>

    <!-- Users Table -->
    <div v-if="users.length" class="table-responsive">
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Status</th>
            <th>Roles</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.active ? 'Active' : 'Blocked' }}</td>
            <td>{{ user.roles.join(', ') }}</td>
            <td>
              <button
                @click="toggleBlockUser(user.id, user.active)"
                :class="user.active ? 'btn btn-danger' : 'btn btn-success'"
              >
                {{ user.active ? 'Block' : 'Unblock' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>No users found.</p>
    </div>

    <!-- Service Management -->
    <h2>Service Management</h2>
    <form @submit.prevent="addService">
      <input v-model="newService.name" placeholder="Service Name" required />
      <input v-model="newService.price" placeholder="Service Price" required />
      <input v-model="newService.time_required" placeholder="Time Required" required />
      <textarea v-model="newService.description" placeholder="Service Description" required></textarea>
      <button type="submit" class="btn btn-primary">Add Service</button>
    </form>

    <ul>
      <li v-for="service in services" :key="service.id">
        {{ service.name }} - {{ service.description }}
        <button @click="updateService(service.id)" class="btn btn-warning">Update</button>
        <button @click="deleteService(service.id)" class="btn btn-danger">Delete</button>
      </li>
    </ul>
  </div>
  `,
  data() {
    return {
      users: [],
      filteredUsers: [],
      searchField: 'email',
      searchText: '',
      services: [],
      newService: {
        name: '',
        price: '',
        time_required: '',
        description: '',
      },
    };
  },
  mounted() {
    this.fetchUsers();
    this.fetchServices();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await fetch("/api/all-users");
        const data = await response.json();
        this.users = data.users;
        this.filteredUsers = data.users;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    filterUsers() {
      if (!this.searchText) {
        this.filteredUsers = this.users;
        return;
      }
      this.filteredUsers = this.users.filter(user => {
        if (this.searchField === 'email') {
          return user.email.toLowerCase().includes(this.searchText.toLowerCase());
        } else if (this.searchField === 'role') {
          return user.roles.some(role => role.toLowerCase().includes(this.searchText.toLowerCase()));
        }
        return false;
      });
    },
    resetFilters() {
      this.searchText = '';
      this.filteredUsers = this.users;
    },
    async toggleBlockUser(userId, isActive) {
      try {
        const action = isActive ? 'block' : 'unblock';
        const response = await fetch(`/api/users/${userId}/${action}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
        });
        const result = await response.json();
        if (response.ok) {
          this.fetchUsers();
          alert(result.message);
        } else {
          alert(`Error: ${result.message}`);
        }
      } catch (error) {
        console.error("Error updating user status:", error);
        alert("An error occurred while updating user status.");
      }
    },
    async fetchServices() {
      try {
        const response = await fetch('/api/services', {
          method: 'GET',
        });
        if (response.ok) {
          this.services = await response.json();
        } else {
          alert('Error fetching services');
        }
      } catch (error) {
        console.error('Error fetching services:', error);
        alert('Error fetching services');
      }
    },
    async addService() {
      try {
        const response = await fetch('/api/services', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.newService),
        });
        const result = await response.json();
        alert(result.message);
        this.newService.name = '';
        this.newService.price = '';
        this.newService.time_required = '';
        this.newService.description = '';
        this.fetchServices();
      } catch (error) {
        console.error('Error adding service:', error);
        alert('Error adding service');
      }
    },
    async updateService(serviceId) {
      const updatedService = prompt(
        'Enter updated service details (name, price, time_required, description):'
      );
      if (!updatedService) return;

      try {
        const [name, price, time_required, description] = updatedService.split(',');
        const response = await fetch(`/api/services/${serviceId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ name, price, time_required, description }),
        });
        const result = await response.json();
        alert(result.message);
        this.fetchServices();
      } catch (error) {
        console.error('Error updating service:', error);
        alert('Error updating service');
      }
    },
    async deleteService(serviceId) {
      try {
        const response = await fetch(`/api/services/${serviceId}`, {
          method: 'DELETE',
        });
        const result = await response.json();
        alert(result.message);
        this.fetchServices();
      } catch (error) {
        console.error('Error deleting service:', error);
        alert('Error deleting service');
      }
    },
  },
};

export default AdminDashboard;
