<!-- InvestmentItem.vue -->
<template>
  <!-- Highlight: Changed from div to tr -->
  <tr class="border-b hover:bg-gray-50 transition-colors">
    <td class="p-3">
      <div class="font-medium">{{ investment.name }}</div>
      <div class="text-sm text-gray-500">{{ investment.ticker_symbol }}</div>
    </td>
    <td class="p-3 text-center">{{ investment.number_of_stocks_owned }}</td>
    <td class="p-3 text-center">{{ investment.average_price_per_unit }}</td>
    <td class="p-3 text-center">{{ investment.current_market_price }}</td>
    <td class="p-3 text-center">{{ ((investment.current_market_price*100 / investment.average_price_per_unit) - investment.average_price_per_unit).toFixed(2) }} % </td>
    <td class="p-3 text-right">{{ formatDate(investment.market_price_refresh_timestamp) }}</td>
  </tr>
</template>

<script>
export default {
  props: {
    investment: Object
  },
  data() {
    return {
    };
  },
  methods: {
    // Highlight: Added method to format date
    formatDate(timestamp) {
      return new Date(timestamp).toLocaleString();
    },
  }
};
</script>