<!-- Form PopUp -->
<template>
  <div> 
    <button @click="showPopup = true" class="text-white px-4 py-2 rounded-md bg-green-500 hover:bg-green-600 transition">
      Buy/Sell Investment
    </button>
    <div v-if="showPopup" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-96">
        <h2 class="text-xl font-semibold mb-4"> Portfolio : {{ selectedPortfolio }}</h2>
        <form @submit.prevent="submitForm">
          
          <div class="flex space-between my-4">
              <div class="container bg-green-500 p-2">
                  <input
                    v-model="formData.action" 
                    id="buy" 
                    type="radio" 
                    value="buy" 
                    required 
                    class="mr-1"
                  >
                  <label for="buy" class="text-lg text-gray-700">Buy</label>
              </div>
              <div class="container bg-red-500 p-2">
                  <input 
                    v-model="formData.action" 
                    id="sell" 
                    type="radio" 
                    value="sell" 
                    required 
                    class="mr-1"
                  >
                  <label for="sell" class="text-lg text-gray-700">Sell</label>
                </div>
              </div>

          <div class="mb-4">
            <label for="tickerSymbol" class="block text-sm font-medium text-gray-700">Ticker Symbol:</label>
            <input v-model="formData.tickerSymbol" id="name" type="text" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50">
          </div>
          <div class="mb-4">
            <label for="averagePrice" class="block text-sm font-medium text-gray-700">Transaction Price Per Unit (Average Buying/Selling Price):</label>
            <input v-model="formData.tranasactionPricePerUnit" id="averagePrice" type="number" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50">
          </div>
          <div class="mb-4">
            <label for="quantity" class="block text-sm font-medium text-gray-700">Buying/Selling Quantity:</label>
            <textarea v-model="formData.transactionQuantity" id="quantity" type= "number" required class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"></textarea>
          </div>

          <div class="flex justify-between">
            <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition">Submit</button>
            <button type="button" @click="showPopup = false" class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition">Cancel</button>
          </div>

        </form>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios';
import { API_APP_URL } from '@/config';

export default {
  name: 'BuyOrSellInvestmentPopUp',
  props: {
    selectedPortfolio: {
        type: String,
        default: ''
    },
    investment: Object,
    
  },
  data() {
    return {
      showPopup: false,
      formData: {
        tickerSymbol: "",
        tranasactionPricePerUnit: 0,
        transactionQuantity: 0,
        action: ""
      }
    };
  },
  methods: {
    submitForm(){
      console.log('emulating Submitting the form: ', this.formData)
      axios.post(`${API_APP_URL}/portfolio/${this.selectedPortfolio}/transaction`,{
        ticker_symbol: this.formData.tickerSymbol.toUpperCase(),
        average_price_per_unit: this.formData.tranasactionPricePerUnit,
        number_of_units: this.formData.transactionQuantity,
        action: this.formData.action
      })
      .then(response => {
        console.log("New Investment Created: ", response)
        this.resetForm();
        this.showPopup = false;
      })
      .catch(error => {
        console.error("error occured: ", error)
      })
    },
    resetForm() {
      this.formData = {
        tickerSymbol: "",
        tranasactionPricePerUnit: "",
        transactionQuantity: "",
        action: ""

      }
    }
  }
};
</script>