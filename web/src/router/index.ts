import { createRouter, createWebHistory } from 'vue-router';
import SaloonEntrance from '../views/SaloonEntrance.vue';
import PokerDashboard from '../views/PokerDashboard.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: SaloonEntrance,
    },
    {
      path: '/poker',
      name: 'poker',
      component: PokerDashboard,
    }
  ],
});

export default router;
