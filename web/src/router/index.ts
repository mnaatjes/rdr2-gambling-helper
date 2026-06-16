import { createRouter, createWebHistory } from 'vue-router';
import SaloonEntrance from '../views/SaloonEntrance.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: SaloonEntrance,
    }
  ],
});

export default router;
