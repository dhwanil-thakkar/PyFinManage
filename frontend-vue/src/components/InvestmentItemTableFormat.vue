<!-- InvestmentItem.vue -->
<template>
  <!-- Highlight: Changed from div to tr -->
  <tr class="border-b hover:bg-gray-50 transition-colors">
    <td class="p-3">
      <div class="font-medium">{{ investment.name }}</div>
      <div class="text-sm text-gray-500">{{ investment.ticker_symbol }}</div>
    </td>
    <td class="p-3 text-right">{{ investment.average_price_per_unit }}</td>
    <td class="p-3 text-right">{{ investment.current_market_price }}</td>
    <td class="p-3 text-right">{{ investment.number_of_stocks_owned }}</td>
    <td class="p-3 text-right">{{ formatDate(investment.market_price_refresh_timestamp) }}</td>
    <td class="p-3 text-center">
      <button @click="toggleExpand" class="text-blue-500 hover:text-blue-700 transition">
        {{ isExpanded ? 'Hide' : 'Buy/Sell' }}
      </button>
    </td>
  </tr>
  <!-- Highlight: Added a new row for the expanded form -->
  <tr v-if="isExpanded" class="bg-gray-50">
    <td colspan="6" class="p-4">
      <div class="flex gap-4 mb-4">
        <input v-model="quantity" type="number" placeholder="Quantity" class="border border-gray-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
        <input v-model="price" type="number" placeholder="Price" class="border border-gray-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
      <div class="flex gap-4">
        <button @click="buyInvestment" class="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition">Buy</button>
        <button @click="sellInvestment" class="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 transition">Sell</button>
      </div>
    </td>
  </tr>
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
    },
    // Highlight: Added method to format date
    formatDate(timestamp) {
      return new Date(timestamp).toLocaleString();
    },
    // Highlight: Add these methods if not already present
    buyInvestment() {
      // Implement buy logic
      console.log('Buy', this.quantity, 'at', this.price);
      this.resetFields();
    },
    sellInvestment() {
      // Implement sell logic
      console.log('Sell', this.quantity, 'at', this.price);
      this.resetFields();
    }
  }
};
</script>