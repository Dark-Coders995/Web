<template>
  <div>
    <AdminNav v-if="isAuthenticated" />
    <br />
    <div v-if="isAuthenticated">
      <form class="productsadd" @submit.prevent="saveproducts">
        <h2>Create New Product</h2>
        <div class="addproducts-form">
          <input v-model="productData.name" type="text" placeholder="Product" required />

          <input
            v-model.number="productData.quantity"
            type="number"
            placeholder="Quantity"
            min="1"
            required
          />

          <input v-model.number="productData.price" type="number" placeholder="Price" required />

          <input v-model="productData.description" type="text" placeholder="Description" />
          <div class="button-container">
            <button type="submit">Save</button>
          </div>
        </div>
      </form>
    </div>
    <div v-else>
      <h1>You need to log in as an admin to access this page..</h1>
    </div>
  </div>
</template>

<script>
import AdminNav from './AdminNav.vue';
import axios from 'axios';

export default {
  name: 'AddProducts',
  components: {
    AdminNav,
  },
  props: ['category_id'], 
  data() {
    return {
      isAuthenticated: false,
      productData: {
        name: '',
        description :'', 
        quantity: '',
        price: '',
      },
    };
  },
  mounted() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
    } else {
      this.isAuthenticated = false;
    }
  },
  methods: {
    saveproducts() { 

      axios
        .post(`http://127.0.0.1:5000/api/admin/product/${this.category_id}`, {
          ...this.productData,
          category_id: this.category_id, 
        },{
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
        .then(response => {
          console.log('Product saved:', response.data);
          window.alert('Product added successfully!');
          this.$router.push({ name: 'productsDash', params: { category_id: this.category_id } });
        })
        .catch(error => {
          console.error('Failed to save products data:', error);
        });
    },
  }
};
</script>

<style>
.productsadd {
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
.addproducts-form input {
  width: 300px;
  height: 40px;
  padding-left: 20px;
  display: block;
  margin-bottom: 30px;
  margin-left: auto;
  margin-right: auto;
  border: 1px solid black;
}
.addproducts-form button {
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
.connect-text {
  position: fixed;
  top: 50%;
  left: 30%;
  font-size: 35px;
  font-weight: auto;
}
</style>
