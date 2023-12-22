<template>
  <div v-if="isAuthenticated">
    <UserNav />
    <div class="container mt-4">
      <template v-if="products.length > 0">
        <div class="product-card-container">
          <div 
          v-for="product in products"
          :key="product.id"
          class="product-card">
            <h3>{{ product.name }}</h3>
            <p> Price : {{ product.price }}</p>
            <p>{{ product.description }}</p>
            <p> Available Quantity : {{ product.quantity }}</p>
            <router-link :to="{ name: 'Booking', params: { category_id: category_id, product_id: product.id } }">
            <button class="buy-now-btn">Buy Product</button>
            </router-link>
          </div>
        </div>
      </template>
      <template v-else>
        <div class="no-products-message">
          <p><u>Sorry! No Products Available </u>😔</p>
        </div>
      </template>
    </div>
  </div>
  <div v-else>
    <h1>You need to login as a User to access this page</h1>
  </div>
</template>

<script>
import axios from 'axios';
import UserNav from './UserNav.vue';

export default {
  name: 'Products',
  components: {
    UserNav
  },
  props: ['category_id'],
  data() {
    return {
      isAuthenticated: false,
      category: {},
      products: []
    };
  },
  created() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
      this.fetchCategory();
      this.fetchProducts();
    } else {
      this.isAuthenticated = false;
    }
  },
  methods: {
    fetchCategory() {
      axios.get(`http://127.0.0.1:5000/api/buy/category/${this.category_id}`, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
        .then(response => {
          this.category = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    fetchProducts() {
      axios.get(`http://127.0.0.1:5000/api/user/category/${this.category_id}/products`,  {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
        .then(response => {
          this.products = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
  }
};
</script>

<style scoped>
.product-card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  margin-top: 20px;
}

.product-card {
  background-color: #b89797; 
  color: #000; 
  margin: 10px; 
}

.product-card h3 {
  font-size: 20px;
  margin-bottom: 10px;
}

.product-card p {
  font-size: 16px;
  margin-bottom: 5px;
}

.no-products-message {
  text-align: center;
  font-size: 30px;
  color: #811212;
  margin-top: 50px;
}

.buy-now-btn {
  cursor: pointer;
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 8px 8px; 
  border-radius: 5px;
  transition: background-color 0.3s;
}

.buy-now-btn:hover {
  background-color: #0056b3;
}


.category-container {
  max-height: calc(100vh - 120px); 
  overflow-y: auto;
  padding-left: 20px;
  padding-right: 20px;
}
</style>
