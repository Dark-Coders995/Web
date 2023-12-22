
const UserPage1 = Vue.component("user_logged",{
    created() {
    const user_id = this.$route.query.user_name;
  },

    data: function(){
        return {
            user: {
        user_name: "" // Replace with actual user data
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
        <router-link v-if="user" to="/user_logged">Home</router-link>
        <router-link v-if="user" to="/">Log Out</router-link>
        <router-link v-if="user" to="/cart">Cart</router-link>
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
                      <router-link v-if="product.quantity !== 0" class="btn btn-primary btn-lg" :to="'/buy/' + product.product_id">Buy</router-link>
                      <p v-else>OUT OF STOCK</p>
                    </li>
                  </ul>
                  <p v-else>No products for this item.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <p v-else>No items in the database.</p>
    </div>
  </div>
    `,

    mounted()
    {
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
    }

});

export default UserPage1;