<template>
    <div id="PortfolioMain" class="flex h-screen">
      <!-- Sidebar for Portfolios -->
      <aside class="w-1/4 bg-gray-100 p-4">
        <Portfolios @portfolio-selected="handlePortfolioSelected" />
      </aside>
      
      <!-- Main Content for Investments -->
      <main class="w-3/4 bg-white p-4">
        <Investments :selectedPortfolioName="selectedPortfolioName" />
      </main>
    </div>
  </template>
  
  <script>
  import Investments from '../components/Investments.vue';
  import Portfolios from '../components/Portfolios.vue';
  
  export default {
    components: {
      Portfolios,
      Investments
    },
    data() {
      return {
        selectedPortfolioName: ''
      };
    },
    methods: {
      handlePortfolioSelected(portfolio) {
        this.selectedPortfolioName = portfolio.name; // Update the selected portfolio name
      }
    }
  };
  </script>
  