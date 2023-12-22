<template>
  <div v-if="isAdmin">
    <AdminNav />
    <div class="container mt-4">
      <div class="position-fixed top-50 start-50 translate-middle">
        <p v-if="products.length === 0" class="connect-text">Please Add Products!</p>
        <router-link v-if="isAdmin" :to="{ name: 'AddProduct', params: { category_id: category_id } }" class="btn btn-primary circular-button">
          +
        </router-link>
      </div>
      <div v-if="products.length > 0" class="myvenue-container mt-5">
        <div class="product-grid">
          <div v-for="product in products" :key="product.id" class="product-card">
            <div class="product-details">
              <h3>{{ product.name }}</h3>
              <p>Price: {{ product.price }}</p>
              <p>{{ product.description }}</p>
              <p>Quantity: {{ product.quantity }}</p>
              
              <div class="button-container">
                <router-link v-if="isAdmin" :to="{ name: 'EditProduct', params: { category_id: category_id, product_id: product.id } }" class="btn btn-secondary">
                  UPDATE
                </router-link>
                <button v-if="isAdmin" class="btn btn-danger" @click="removeproduct(product.id)" style="margin-left: 10px;">
                  REMOVE</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <h1>You need to log in as an admin to access this page.</h1>
  </div>
</template>

<script>
import axios from "axios";
import AdminNav from './AdminNav.vue';

export default { 
  name: 'ProductDash',
  components: {
    AdminNav
  },
  props: ['category_id'],
  data() {
    return {
      isAdmin: false,
      products: []
    };
  },
  mounted() {
    this.fetchproducts()
  },
  methods: {
    fetchproducts() {
      const token = localStorage.getItem('access_token');

      axios.get(`http://127.0.0.1:5000/api/admin/product/${this.category_id}`, {
        headers: { 'Authorization': 'Bearer ' + token }
      })
        .then(response => {
          this.products = response.data.Products;
          this.isAdmin=true;
        })
        .catch(error => {
          console.error(error);
          this.isAdmin=false;
        });
    },
    removeproduct(ProductId) {
      axios.delete(`http://127.0.0.1:5000/api/admin/product/${this.category_id}/${ProductId}`, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
        .then(response => {
          this.products = this.products.filter(product => product.id !== ProductId);
          console.log('Product removed:', response.data);
        })
        .catch(error => {
          console.error('Failed to remove Product:', error);
        });
    }
  }
};
</script>

<style>
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}
.circular-button {
  width: 100px;
  height: 100px;
  border-radius: 70%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  background-color: #007bff;
  color: #ffffff;
  cursor: pointer;
  position: fixed;
  top: 55%;
  left: 75%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  transition: 0.3s;
}

.product-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #ccc;
  background-color: antiquewhite;
  border-radius: 5px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.product-image {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  border-radius: 5px;
}

.product-details {
  margin-top: 10px;
  text-align: center;
}

.product-details h3 {
  font-size: 20px;
  margin-bottom: 5px;
}

.product-details p {
  margin: 0;
  font-size: 16px;
}

.button-container {
  margin-top: 10px;
}

.button-container button {
  margin-right: 10px;
}

.myvenue-container {
  padding-top: 40px;
  padding-bottom: 10px;
}
</style>
