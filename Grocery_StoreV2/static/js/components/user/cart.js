const UserPage4 = Vue.component("cart", {

    data: function () {
        return {
            user: {
                user_name: "John Doe" // Replace with actual user data
            },
            cart_items:[],
            total_price: 0
        }
    },
    template: `
   <div>
    <nav>
      <h1>Grocery Store</h1>
      <div class="navbar-nav">
        <span v-if="user">Logged in as: {{ user.user_name }}</span>
        <router-link v-if="user" to="/user_logged">Home</router-link>
        <router-link v-if="user" to="/">Log Out</router-link>
        <router-link v-if="user" to="/cart">Cart</router-link>
      </div>
    </nav>

    <h1 style="padding: 10px">Welcome, {{ user.user_name }}!</h1>
    <h2 style="padding: 10px">Your Cart:</h2>

    <table>
      <tr>
        <th>Product Name</th>
        <th>Quantity</th>
        <th>Unit Price</th>
        <th>Total Price</th>
        <th>Actions</th>
        <th>Availability</th>
      </tr>

      <tr v-for="cart_item in cart_items" :key="cart_item.cart_id">
        <td>{{ cart_item.product.product_name }}</td>
        <td>
          <input name="cart_item_id" type="hidden" :value="cart_item.cart_id">
          {{ cart_item.quantity }}
          <br>
          <template v-if="cart_item.quantity < cart_item.product.quantity">
            <router-link :to="'/update_cart/' + cart_item.product_id">Update</router-link>
          </template>
          <template v-else>
            <p>OUT OF STOCK</p>
          </template>
        </td>
        <td>{{ cart_item.product.rate }}</td>
        <td>{{ cart_item.total_price }}</td>
        <td>
          <form >
            <input name="cart_item_id" type="hidden" :value="cart_item.cart_id">
            <input name="user_id" type="hidden" :value="cart_item.user.id">
            <input name="product_id" type="hidden" :value="cart_item.product_id">
            <input name="action" type="hidden" value="remove">
            <button type="submit">Remove</button>
          </form>
        </td>
        <td>{{ cart_item.product.quantity }}</td>
      </tr>
    </table>

    <br>
    <p>Total Price: {{ total_price }}</p>
  </div>
   `,
    mounted() {
        this.getCart();
    },
    getCart() {
        var url = "/api/cart"
        fetch(url, {
            //headers: {
            //'x-access-tokens': localStorage.getItem('auth_token')
            //},
        })
            .then(response => {
                if (response.ok) {
                    response.json().then(data => {
                        this.cart_items = data;
                    })
                }
            });
    },
});
export default UserPage4;