const Page3 = Vue.component("login",{

    template: `
        <div class="login-card">
            <h2 class="text-center mb-4">Manager Login</h2>
            <form @submit.prevent="login">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input class="form-control" id="username" name="username" required type="text">
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input class="form-control" id="password" name="password" required type="password">
                </div>
                <button class="btn btn-primary w-100" type="submit">Login</button>
            </form>
            <p class="mt-3"><router-link to="/">User Login</router-link></p>
        </div>
        `,
    methods:{
        login(){
            this.$router.push('/manager_logged')
        }
    },

});

export default Page3;
