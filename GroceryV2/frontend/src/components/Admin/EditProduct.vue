<template>
  <div v-if="isAuthenticated">
    <AdminNav />
    <br />
    <div class="productadd">
      <h2>Edit Product</h2>
      <form @submit.prevent="saveproduct">
        <div class="addproduct-form">
          <input v-model="ProductData.name" type="text" placeholder="Name" />
          <input v-model="ProductData.description" type="text" placeholder="Description" />
          <input v-model="ProductData.quantity" type="number" placeholder="Quantity" />
          <input v-model="ProductData.price" type="number" placeholder="Price" />
          <div class="button-container">
            <button type="submit">Save</button>
          </div>
        </div>
      </form>
    </div>
  </div>
  <div v-else>
    <h1>You need to log in as an admin to access this page.</h1>
  </div>
</template>

<script>
import AdminNav from './AdminNav.vue'
import axios from "axios";

export default {
  name: 'EditProduct',
  components: {
    AdminNav
  },
  props: ['category_id', 'product_id'],
  data() {
    return {
      isAuthenticated: false,
      ProductData: {
        name: '',
        description: '',
        quantity: 0,
        price: 0,
      }
    };
  },
  mounted() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
      this.fetchproductData();
    } else {
      this.isAuthenticated = false;
    }
  },
  methods: {
    fetchproductData() {
      axios.get(`http://127.0.0.1:5000/api/admin/product/${this.category_id}/${this.product_id}`)
        .then(response => {
          this.ProductData = response.data.Product;
        })
        .catch(error => {
          console.error('Failed to fetch Product:', error);
        });
    },
    saveproduct() {
      if (!this.isAuthenticated) {
        window.alert('Please log in as an admin to edit the product.');
        return;
      }

      axios.put(`http://127.0.0.1:5000/api/admin/product/${this.category_id}/${this.product_id}`, this.ProductData, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
      .then(response => {
        console.log('Product updated:', response.data);
        this.$router.push({ name: 'ProductDash', params: { category_id: this.category_id } });
      })
      .catch(error => {
        console.error('Failed to update product:', error);
      });
    }
  }
};

</script>

<style>
.productadd {
  position: fixed;
  top: 53%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 400px;
  padding: 20px;
  background-color: #ddaeae;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.addproduct-form input {
    width: 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 30px;
    margin-left: auto;
    margin-right: auto;
    border: 1px solid black;
}
.addproduct-form button {
    align-self: center;
    width: 200px;
    height: 40px;
    border: blue;
    color: gainsboro;
    background-color: black;
    cursor: pointer;
}
.button-container {
  display: flex;
  justify-content: center;
  width: 100%;
}
</style>
