const ManagerPage1 = Vue.component("manager_logged", {

    data: function () {
        return {
            user: {
                user_name: "Admin" // Replace with actual user data
            },
            categories: []
        }
    },
    template: `
    <div>
        <nav>
            <h1>Grocery Store</h1>
        <div class="navbar-nav">
        <span v-if="user" class="navbar-text">Logged in as: {{ user.user_name }}</span>
        <router-link v-if="user" to="/">Log Out</router-link>
        </div>
        </nav>

    <div class="container">
      <h2>Welcome, {{ user.user_name }}!</h2>
    </div>
    
    

    <div class="container">
      <h1 class="my-4">Category</h1>
      <div v-if="categories.length > 0" class="row">
        <div v-for="category in categories" :key="category.category_id" class="col-md-4 mb-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ category.category_name }}</h5>
              <div class="card mt-3">
                <div class="card-body">
                  <h6 class="card-title">Products</h6>
                  <ul v-if="category.products.length > 0" class="list-group">
                    <li v-for="product in category.products" :key="product.product_id" class="list-group-item">
                      Name : {{ product.product_name }}
                      <br>
                      Quantity: {{ product.quantity }}
                      <br>
                      Rate: {{ product.rate }} {{ product.unit }}
                      <br>
                      Total price : {{ product.rate  *  product.quantity }}
                      <br>
                      <div class="col">
                        <router-link :to="'/update_product/' + product.product_id" class="btn btn-primary w-100">Update Product</router-link>
                      </div>
                      <div class="col">
                        <button @click="deleteProduct(product.product_id)" class="btn btn-danger btn-sm" type="button">Delete Product</button>
                      </div>
                    </li>
                  </ul>
                  <p v-else>No products for this item.</p>
                </div>
                <div class="col">
                    <router-link :to="'/add_product/' + category.category_id">Add Product</router-link>
                </div>
              </div>
              <div class="col">
                        <button @click="deleteCategory(category.category_id)" class="btn btn-danger btn-sm" type="button">Delete Category</button>
                      </div>
              <div class="col">
                        <router-link :to="'/update_category/' + category.category_id" class="btn btn-primary w-100">Update Category</router-link>
                      </div>
            </div>
          </div>
        </div>
      </div>
      <p v-else>No items in the database.</p>
    </div>
    
    <router-link to="/add_category">Add Category</router-link>
    <button @click="celery_job">CSV Report</button>

  </div>
    `,
    mounted() {
        this.getCategory();
    },
    methods: {
        getCategory() {
            var url = "/api/category"
            fetch(url, {
                //headers: {
                //'x-access-tokens': localStorage.getItem('auth_token')
                //},
            })
                .then(response => {
                    if (response.ok) {
                        response.json().then(data => {
                            this.categories = data;
                        })
                    }
                });
        },

        deleteCategory(category_id) {
            var url = `/api/manager/delete_category/${category_id}`;
            fetch(url, {
                method: 'DELETE',
                // Add headers if needed
            })
                .then(response => {
                    if (response.ok) {
                        window.location.reload();
                    }
                })
                .catch(error => {
                    console.error('Error deleting Category:', error);
                });
        },


        deleteProduct(product_id) {
            var url = `/api/manager/delete_product/${product_id}`;
            fetch(url, {
                method: 'DELETE',
                // Add headers if needed
            })
                .then(response => {
                    if (response.ok) {
                        // Product successfully deleted, update UI as needed
                        // For example, remove the product from its category's products array
                        window.location.reload();
                    }
                })
                .catch(error => {
                    console.error('Error deleting product:', error);
                });
        },
        celery_job : function () {
            fetch('/trigger-celery').then(r => r.json()).then(d => {
                console.log("Celery Drtails", d)
                window.location.href = "/download"
            })
        }
    },

});

export default ManagerPage1;
