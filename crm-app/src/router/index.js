import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/AboutView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/emp_home",
      name: "emp_home",
      component: () => import("../components/EmployeeHome.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/ex_cust",
      name: "Ex_Cust",
      component: () => import("../views/ViewCustomer.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/TaskPage",
      name: "TaskPage",
      component: () => import("../views/TasksPage.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/AddCustomer",
      name: "AddCustomer",
      component: () => import("../views/AddCustomer.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/Login.vue"),
    },
  ],
});

//Global route guard
router.beforeEach((to, from, next) => {
  const user = JSON.parse(sessionStorage.getItem("user"));

  if (to.meta.requiresAuth && !user) {
    // Redirect to login if trying to access a protected route
    next({ name: "login" });
  } else {
    next(); // Allow navigation
  }
});

export default router;
