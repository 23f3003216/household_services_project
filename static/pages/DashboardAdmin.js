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
  </div>
  `,
  data() {
    return {
      users: [],
      filteredUsers: [],
      searchField: 'email',
      searchText: '',
    };
  },
  mounted() {
    this.fetchUsers();
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
  },
};

export default AdminDashboard;
