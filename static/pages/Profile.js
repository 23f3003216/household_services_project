const Profile = {
    template: `
      <div>
        <h1>Your Profile</h1>
        <p>Welcome, {{ currentUser.email }}</p>
        <p>Role: {{ currentUser.roles[0].description }}</p>
        <router-link to="/admin-dashboard" v-if="currentUser.roles[0].name === 'admin'">Admin Dashboard</router-link>
        <router-link to="/service-dashboard" v-if="currentUser.roles[0].name === 'service'">Service Dashboard</router-link>
        <router-link to="/customer-dashboard" v-if="currentUser.roles[0].name === 'customer'">Customer Dashboard</router-link>
      </div>
    `,
  };
  
  export default Profile;

  