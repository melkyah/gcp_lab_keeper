import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";

Vue.use(Router);

const router = new Router({
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
      meta: {
        title: "GCP Lab Keeper"
      }
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: function() {
        return import(/* webpackChunkName: "about" */ "./views/About.vue");
      }
    }
  ]
});

router.afterEach((to, from) => {
  document.title = to.meta.title;
});

export default router;
