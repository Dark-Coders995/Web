import Page1 from "./components/login.js";
import Page2 from "./components/sign_up.js";
import Page3 from "./components/manager_login.js";
import UserPage1 from "./components/user/user_logged.js";
import UserPage2 from "./components/user/update_cart.js";
import UserPage3 from "./components/user/buy.js";
import UserPage4 from "./components/user/cart.js";
import ManagerPage1 from "./components/manager/manager_logged.js";
import ManagerPage2 from "./components/manager/update_category.js";
import ManagerPage3 from "./components/manager/add_category.js";
import ManagerPage4 from "./components/manager/add_product.js";
import ManagerPage5 from "./components/manager/update_product.js";


const routes = [
    { path: '/', component: Page1 },
    { path : '/sign_up' , component: Page2 },
    { path : '/manager_login' , component: Page3 },


    {path : '/user_logged' , component: UserPage1},
    {path : '/update_cart' , component: UserPage2},
    {path : '/buy/:product_id' , component: UserPage3},
    {path : '/cart' , component: UserPage4},


    {path : '/manager_logged' , component: ManagerPage1},
    {path : '/update_category/:category_id', component: ManagerPage2 },
    {path : '/add_category' , component: ManagerPage3},
    {path : '/add_product/:category_id' ,component: ManagerPage4},
    {path : '/update_product/:product_id' , component: ManagerPage5}
];

const router = new VueRouter({
    routes
});
export  default router