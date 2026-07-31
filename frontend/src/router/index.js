import { createRouter, createWebHistory } from 'vue-router'

// Импортируем страницы
import HomePage from '../views/home/HomePage.vue'
import ConsultasPage from "../views/consultas/ConsultasPage.vue";
import ContactoPage from "../views/contacto/ContactoPage.vue";
import BlogPage from "../views/blog/BlogPage.vue";
import TiendaPage from "../views/tienda/TiendaPage.vue";
import CarritoPage from "../views/carrito/CarritoPage.vue";
import CuentaPage from "../views/cuenta/CuentaPage.vue";
import LegalPage from "../views/legal/LegalPage.vue";
import ComprasPage from "../views/compras/ComprasPage.vue";
import ProductoPage from "../views/producto/ProductoPage.vue";
import LoginPage from "../views/auth/LoginPage.vue";
import RegisterPage from "../views/auth/RegisterPage.vue";
import BlogPostPage from "../views/blog/BlogPostPage.vue";
import OrderPage from "../views/order/OrderPage.vue";
import EstudianteCabinetPage from "../views/escuela/EstudianteCabinetPage.vue";
import ProfesorCabinetPage from "../views/escuela/ProfesorCabinetPage.vue";

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/consultas',
    name: 'Consultas',
    component: ConsultasPage
  },
  {
    path: '/contacto',
    name: 'Contacto',
    component: ContactoPage
  },
  {
    path: '/blog',
    name: 'Blog',
    component: BlogPage
  },
  {
    path: '/tienda',
    name: 'Tienda',
    component: TiendaPage
  },
  {
    path: '/carrito',
    name: 'Carrito',
    component: CarritoPage
  },
  {
    path: '/cuenta',
    name: 'Cuenta',
    component: CuentaPage
  },
  {
    path: '/legal',
    name: 'Legal',
    component: LegalPage
  },
  {
    path: '/compras',
    name: 'Compras',
    component: ComprasPage
  },
  {
    path: '/producto/:id',
    name: 'Producto',
    component: ProductoPage
  },
    {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { guest: true }  // Только для неавторизованных
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage,
    meta: { guest: true }
  },
  {
    path: '/blog/:slug',
    name: 'BlogPost',
    component: BlogPostPage,
  },
  {
    path: '/order/:orderNumber',
    name: 'Order',
    component: OrderPage,
  },
  {
    // Контроль доступа по роли (student) - внутри компонента, см.
    // EstudianteCabinetPage.vue onMounted(). Данные курсов - заглушка,
    // ждём school API (Неделя 2 плана, см. PLAN_ETAP2.md).
    path: '/escuela/estudiante',
    name: 'EstudianteCabinet',
    component: EstudianteCabinetPage,
  },
  {
    // Контроль доступа по роли (teacher) - внутри компонента, см.
    // ProfesorCabinetPage.vue onMounted().
    path: '/escuela/profesor',
    name: 'ProfesorCabinet',
    component: ProfesorCabinetPage,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router