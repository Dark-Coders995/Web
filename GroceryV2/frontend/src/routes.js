import Login from './components/User/UserLogin.vue'
import SignUp from './components/User/SignUp.vue'
import AdminLogin from './components/Admin/AdminLogin.vue'
import UserDash from './components/User/UserDash.vue'
import AdminDash from './components/Admin/AdminDash.vue'
import Booking from './components/User/Booking.vue'
import AdminSignup from './components/Admin/AdminSignup.vue'
import ProductDash from './components/Admin/ProductDash.vue'
import BookingDashboard from './components/User/BookDash.vue'
import SearchVenue from './components/User/SearchDash.vue'
import Summary from './components/Admin/Summary.vue'
import { createRouter, createWebHistory } from 'vue-router'
import AddCategory from './components/Admin/AddCategory.vue'
import AddProduct from './components/Admin/AddProduct.vue'
import EditProduct from './components/Admin/EditProduct.vue'
import EditCategory from './components/Admin/EditCategory.vue'
import PostedShows from './components/User/Products.vue'
import Products from './components/User/Products.vue'
const routes = [
    {
        path: '/',
        redirect: '/Login',
    },
    {
        name: 'Login',
        component: Login,
        path: '/Login'
    },
    {
        name: 'SignUp',
        component: SignUp,
        path: '/sign-up'
    },
    {
        name: 'AdminLogin',
        component: AdminLogin,
        path: '/admin-login'
    },
    {
        name: 'UserDash',
        component: UserDash,
        path: '/userdash'
    },
    {
        name: 'AdminDash',
        component: AdminDash,
        path: '/admindash'
    },
    {
        name: 'AddCategory',
        component: AddCategory,
        path: '/addcategory'
    },
    {
        name: 'AddProduct',
        component: AddProduct,
        path: '/addproduct/:category_id',
        props: true
    },
    {
        name: 'EditCategory',
        component: EditCategory,
        path: '/editcategory/:category_id',
        props: true
    },
    {
        name: 'EditProduct',
        component: EditProduct,
        path: '/editshow/:category_id/:product_id',
        props: true
    },
    {
        name: 'Booking',
        component: Booking,
        path: '/booking/:category_id/:product_id',
        props: true
    },
    {
        name: 'AdminSignup',
        component: AdminSignup,
        path: '/adminsignup'
    },
    {
        name: 'ProductDash',
        component: ProductDash,
        path: '/product/:category_id',
        props: true
    },
    {
        name: 'Products',
        component: Products,
        path: '/category/:category_id/products',
        props: true
    },
    {
        name: 'BookingDashboard',
        component: BookingDashboard,
        path: '/bookings',
    },
    {
        name: 'SearchDash',
        component: SearchVenue,
        path: '/search',
    },
    {
        name: 'Summary',
        component: Summary,
        path: '/summary',
    }


]


const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
