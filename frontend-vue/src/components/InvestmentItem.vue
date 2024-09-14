<template>
    <div class="investment-item p-6 bg-white rounded-lg shadow-md transition-transform transform hover:scale-105">
      <div class="investment-info p-4">
        <h3 class="text-xl font-semibold text-gray-800">{{ investment.name }} ({{ investment.ticker_symbol }})</h3>
        <p class="text-gray-600">Average Price Per Unit: <span class="font-medium">{{ investment.average_price_per_unit }}</span></p>
        <p class="text-gray-600">Current Market Price: <span class="font-medium">{{ investment.current_market_price }}</span></p>
        <p class="text-gray-600">Number of Stocks Owned: <span class="font-medium">{{ investment.number_of_stocks_owned }}</span></p>
        <p class="text-gray-600">Last Updated: <span class="font-medium">{{ new Date(investment.market_price_refresh_timestamp).toLocaleString() }}</span></p>
      </div>
  
      <button @click="toggleExpand" class="mt-4 w-full py-2 px-4 bg-blue-500 text-white rounded hover:bg-blue-600 transition">
        {{ isExpanded ? 'Hide Form' : 'Buy/Sell' }}
      </button>
  
      <div v-if="isExpanded" class="expanded-form mt-4 p-4 border-t border-gray-200">
        <div class="flex gap-4 mb-4">
          <input v-model="quantity" type="number" placeholder="Quantity" class="border border-gray-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="price" type="number" placeholder="Price" class="border border-gray-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div class="flex gap-4">
          <button @click="buyInvestment" class="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition">Buy</button>
          <button @click="sellInvestment" class="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 transition">Sell</button>
        </div>
      </div>
    </div>
  </template>

  <script>
  export default {
    props: {
      investment: Object
    },
    data() {
      return {
        isExpanded: false,
        quantity: 0,
        price: 0
      };
    },
    methods: {
      toggleExpand() {
        this.isExpanded = !this.isExpanded;
      },
      resetFields() {
        this.quantity = 0;
        this.price = 0;
      }
    }
  };
  </script>
  