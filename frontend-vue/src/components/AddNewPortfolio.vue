<!-- AddNewPortfollio.vue -->>
<template>
    <div id="AddPortfolio" class="border mt-10 p-4 rounded-lg shadow-lg flex flex-col">
        <!-- <h2 class="text-lg font-semibold mb-4">Manage Your Portfolios</h2> -->       
        <button 
          @click="toggle" 
          class="border p-2 text-white bg-black rounded">
          {{ addPortfolioToggle ? 'close' : 'Add New Portfolio' }}
        </button>

        <form v-if="addPortfolioToggle" @submit.prevent="createNewPortfolio" class="mt-4 flex flex-col">
          <label class="block mb-2" for="portfolioName"> Create new Portfolio :</label>
          <input 
            id="portfolioName"
            v-model="newPortfolioName" 
            placeholder="Portfolio Name" 
            required
            class="border rounded-md p-2 w-full"
          />
          <button 
            type="submit" 
            class="mt-2 border p-2 text-white bg-green-500 hover:bg-green-600 rounded">
            Create New Portfolio
          </button>
        </form>

        <!-- Success Message -->
        <div v-if="successMessage" class="mt-4 text-green-600">
          {{ successMessage }}
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="mt-4 text-red-600">
          {{ errorMessage }}
        </div>
      </div>
</template>

<script>
  import { API_APP_URL } from '@/config';
  import axios from 'axios';

  export default {
    data() {
      return {
        newPortfolioName: "",
        addPortfolioToggle: false,
        successMessage: "",
        errorMessage: "",
      };
    },
    methods: {
      createNewPortfolio() {
        axios.post(`${API_APP_URL}/create-new-portfolio/?name=${this.newPortfolioName}`)
        .then(response => {
        console.log("New portfolio created sucessfully");
        this.successMessage = "New Portfolio Created Successfully!";
        this.errorMessage = "";
        this.newPortfolioName = "";
        this.addPortfolioToggle = false;

        this.$emit('portfolio-added')

        setTimeout(() => {
            this.successMessage = "";
        }, 5000);
        })
        .catch(error => {
        console.error('Error:', error );
        this.errorMessage = "An error occured creating the portfolio, please try again";
        this.successMessage = "";

        setTimeout(() => {
            this.errorMessage = "";
        }, 5000);
        });
      },
      toggle(){
        this.addPortfolioToggle = !this.addPortfolioToggle
      },
      selectPortfolio(portfolio) {
        this.$emit('portfolio-selected', portfolio); // Emit an event with the selected portfolio
      }
    }
  };
</script>