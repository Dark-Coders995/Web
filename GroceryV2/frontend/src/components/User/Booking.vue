<template>
  <div>
    <UserNav v-if="isAuthenticated" />
    <div v-if="!loading">
      <div v-if="availableProducts > 0"> 
        <div class="bookingadd">
          <button v-if="product" v-text="`Available Products: ${ availableProducts }`"></button>
          <div class="addbooking-form" v-if="product">
            <h3> Buy </h3>
            <label for="Number">Quantity </label>
            <input type="number" v-model="boughtProducts" @input="calculateTotal" />
            <label for="Price">Price</label>
            <input type="text" :value="price" readonly />
            <label for="Total">Total</label>
            <input type="text" :value="total" readonly />
            <div class="button-container">
              <button @click="buyProducts">Buy Products </button>
            </div>
            <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          </div>
        </div>
      </div>
      <div v-else class="housefull-popup"> 
        <h5>No Products Available</h5>
        <button @click="goBack">Go Back</button>
      </div>
    </div>
  </div>
</template>

<script>
import UserNav from './UserNav.vue';
import axios from 'axios';

export default {
  name: 'Booking',
  components: {
    UserNav,
  },
  props: ['category_id', 'product_id'],
  data() {
    return {
      isAuthenticated: false,
      category: {},
      product: null,
      boughtProducts: 0,
      availableProducts: undefined,
      price: 0,
      total: 0,
      errorMessage: '',
      loading: true, 
    };
  },
  created() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
      this.fetchData();
    } else {
      this.isAuthenticated = false;
    }
  },
  methods: {
    fetchData() {
      axios
        .get(`http://127.0.0.1:5000/api/buy/category/${this.category_id}`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') },
        })
        .then((response) => {
          this.category = response.data;
          this.fetchproduct();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    fetchproduct() {
      axios
        .get(`http://127.0.0.1:5000/api/buy/category/${this.category_id}/product/${this.product_id}`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') },
        })
        .then((response) => {
          this.product = response.data;
          this.getavailableProducts(); 
          this.price = this.product.price;
          this.calculateTotal();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getavailableProducts() {
      axios
        .get(`http://127.0.0.1:5000/api/buy/product/${this.product_id}`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') },
        })
        .then((response) => {
          this.availableProducts = response.data.available_product;
        })
        .catch((error) => {
          console.error(error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    calculateTotal() {
      this.total = this.boughtProducts * this.price;
    },
    buyProducts() {
      if (!this.isAuthenticated) {
        console.error('User not authenticated.');
        return;
      }

      const postData = {
        quantity: this.boughtProducts,
      };

      axios
        .post(
          `http://127.0.0.1:5000/api/user/category/${this.category_id}/product/${this.product_id}/buy`,
          postData,
          {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') },
          }
        )
        .then((response) => {
          console.log('Bought successful:', response.data.message);
          this.errorMessage = '';
          alert('Congratulations!');
          this.fetchproduct();
          this.$router.push(`/category/${this.category_id}/products`);
        })
        .catch((error) => {
          console.error('Error While Buying:', error);
          this.errorMessage = error.response.data.message || 'An error occurred during booking.';
        });
    },
    goBack() {
      this.$router.push(`/postedshows/${this.category_id}/shows`);
    },
  },
  watch: {
    product: {
      handler() {
        this.getavailableProducts(); 
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.bookingadd {
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

.addbooking-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.addbooking-form input {
  width: 300px;
  height: 40px;
  padding-left: 20px;
  display: block;
  margin-bottom: 30px;
  margin-left: auto;
  margin-right: auto;
  border: 1px solid rgb(184, 17, 17);
}

.addbooking-form button {
  width: 200px;
  height: 40px;
  border: none;
  color: rgb(247, 242, 242);
  background-color: black;
  cursor: pointer;
}

.error-message {
  color: rgb(236, 111, 111);
}

.housefull-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 400px;
  padding: 20px;
  background-color: #bb9088;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(8, 0, 0, 0.815);
}

.housefull-popup h3 {
  margin-bottom: 20px;
}

.housefull-popup button {
  width: 150px;
  height: 40px;
  border: none;
  color: rgb(255, 253, 253);
  background-color: rgb(196, 47, 47);
  cursor: pointer;
}
</style>
