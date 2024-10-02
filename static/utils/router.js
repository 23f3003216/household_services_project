import Home from "../pages/Home.js";
import Signup from "../pages/Signup.js";
import DashboardAdmin from "../pages/DashboardAdmin.js";
import DashboardServiceProfessional from "../pages/DashboardServiceProfessional.js";
import DashboardCustomer from "../pages/DashboardCustomer.js";
import Services from "../pages/Services.js";
import BookService from "../pages/BookService.js";
import Login from "../pages/Login.js";
import Profile from "../pages/Profile.js";


const routes = [
  { path: "/", component: Home }, 
  { path: "/login", component: Login }, 
  { path: "/profile", component: Profile }, 
  { path: "/signup", component: Signup }, 
  { path: "/admin-dashboard", component: DashboardAdmin }, 
  { path: "/service-dashboard", component: DashboardServiceProfessional },
  { path: "/customer-dashboard", component: DashboardCustomer }, 
  { path: "/services", component: Services }, 
  { path: "/book-service", component: BookService } 
];

const router = new VueRouter({
  mode: 'history',
  routes, 
});


export default router;