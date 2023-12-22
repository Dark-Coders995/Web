const UserPage3 = Vue.component("buy", {

    data: function () {
    return {
      formData: {
        buy_quantity: 0
      },
      product: {
        product_name: "",
          quantity:0 ,
        rate:0 ,
        unit: "" ,
        category: {
          category_name: ""
        },
      },
      totalPrice: 0 ,
      isQuantityValid: true
    }
  },


    template :`
    <div class="login-card">
    <h2 class="text-center mb-4">Buy {{ product.product_name }} from {{ product.category.category_name }}</h2>
    <h3 class="text-center mb-4"> Available {{ product.quantity }}</h3>
    <form @submit.prevent="buyProduct">
      <div class="form-group">
        <label for="buy_quantity">Quantity</label>
        <input v-model="formData.buy_quantity" class="form-control" id="buy_quantity" name="buy_quantity" @input="updateTotalPrice" required type="number" :value="formData.buy_quantity"> {{ product.unit }}
      </div>
      <p>Price / unit: {{ product.rate }}</p>
      <p>Total Price: <span id="total_price">{{ totalPrice.toFixed(2) }}</span></p>
      <button v-if="product.quantity >= formData.buy_quantity" class="btn btn-primary w-100" type="submit">Buy</button>
      <p v-else>Not enough available quantity to buy</p>
    </form>
  </div>
    `,

    mounted()
    {
        this.getProduct();
        this.updateTotalPrice();
        this.buyProduct();
    },
  methods: {
    updateTotalPrice() {
      const quantity = this.formData.buy_quantity;
      this.totalPrice = this.product.rate * quantity;
      this.isQuantityValid = quantity >= 1 && quantity <= this.product.quantity;
    },

    getProduct(){
            const product_id = this.$route.params.product_id;
            var url = `/api/buy/${product_id}`;
      fetch(url, {
        //headers: {
          //'x-access-tokens': localStorage.getItem('auth_token')
        //},
      })
        .then(response => {
          if (response.ok) {
            response.json().then(data => {
               this.product = data;
            })
          }
        });
        },

    buyProduct() {
     if (this.isQuantityValid) {
         const product_id = this.$route.params.product_id;
        const url = `/api/buy/${product_id}`;

        fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({buy_quantity: this.formData.buy_quantity})
            }).then(response => {
                if (!response.ok) {
                    response.json().then(data => {
                        if (!response.ok) {
                          throw new Error('Network response was not ok');
                        }
                    return response.text();
                    })
                }
                else if (response.ok) {
                   //response.json().then(data =>
            //localStorage.setItem('auth_token', data['token']));
                    this.$router.push('/user_logged');
                }
            })
        // Add your logic to handle the form submission (e.g., sending an API request)
      }
    }
  }
});
export default UserPage3;