const ManagerPage4 = Vue.component("add_product",{

    data: function () {
    return {
      errorMessage: "",
      productName: "",
      rate: 0,
      quantity: 0,
      unit: "rs/gram",
      error: false,
      error_3: false,
      error_2 : false
    }
  },

    template: `
       <div class="login-card">
    <h2 class="text-center mb-4">Add Product</h2>
    <form @submit.prevent="addProduct">
      <div class="form-group">
        <label for="product_name">Product Name</label>
        <input v-model="product_name" class="form-control" id="product_name" required type="text">
      </div>
      <div class="form-group">
        <label for="rate">Rate</label>
        <input v-model="rate" class="form-control" id="rate" required step="0.01" type="number">
      </div>
      <div class="form-group">
        <label for="quantity">Quantity</label>
        <input v-model="quantity" class="form-control" id="quantity" required type="number">
      </div>
      <div class="form-group">
        <label for="unit">Unit</label>
        <select v-model="unit" class="form-control" id="unit" required>
          <option value="rs/gram">rs/gram</option>
          <option value="rs/litre">rs/litre</option>
          <option value="rs/dozen">rs/dozen</option>
          <option value="rs/kg">rs/kg</option>
        </select>
      </div>
      <button class="btn btn-primary w-100" type="submit">Add Product</button>
    </form>
  </div>
    `,
    methods: {
        addProduct: function (event) {
            this.error = "";
            const category_id = this.$route.params.category_id;
            var url = `/api/manager/add_product/${category_id}`;
            console.log(url);

            fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({product_name: this.product_name, rate: this.rate, quantity: this.quantity, unit: this.unit})
            }).then(response => {
                if (!response.ok) {
                    response.json().then(data => {
                        this.error = data["error_message"]
                        if (data["error_code"] == "BE104") {
                            this.error = true
                            this.rate = 0
                            this.$refs.rate.focus();
                        } else if (data["error_code"] == "BE105") {
                            this.error_1 = true
                            this.product_name = ""
                            this.$refs.productName.focus()
                        } else if (data["error_code"] == "BE106") {
                            this.error_2 = true
                            this.quantity = 0
                            this.$refs.quantity.focus();
                        }
                    })
                }
                else if (response.ok) {
                   //response.json().then(data =>
                     //  localStorage.setItem('auth_token', data['token']));
                   this.$router.push('/manager_logged');
                }
            })
        },
    }
});

export default ManagerPage4;
