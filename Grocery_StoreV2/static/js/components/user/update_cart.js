const UserPage2 = Vue.component("update_cart",{

    data:function (){
        return{
            formData: {
        update_quantity: ""
      },
      product: {
        product_id: 1, // Replace with actual product ID
        quantity: 10 // Replace with actual quantity
      }
        }
    },
   template:`
   <div class="login-card">
    <h2 class="text-center mb-4">Update Cart</h2>
    <form @submit.prevent="updateCart">
      <div class="form-group">
        <label for="update_quantity">Quantity</label>
        <input v-model="formData.update_quantity" class="form-control" id="update_quantity" name="update_quantity" required type="number"
               :value="product.quantity" :min="1" :max="product.quantity">
      </div>
      <button class="btn btn-primary w-100" type="submit">Update Product</button>
    </form>
  </div>
   `,

});

export  default UserPage2;