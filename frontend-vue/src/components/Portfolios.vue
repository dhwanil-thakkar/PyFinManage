<!-- Portfolios.vue -->


<template>
    <div id="PortfolioContainer" class="container p-4">
      <h1 class="text-2xl font-bold m-4 p-4">Portfolios</h1>
      <div id="portfolios" class="space-y-4 m-4 p-4">
        <div v-for="portfolio in portfolios" :key="portfolio.portfolio_id" 
             class="p-4 bg-white shadow-md rounded-md" @click="selectPortfolio(portfolio)">
          <h2 class="text-xl font-semibold">{{ portfolio.name }}</h2>
          <p class="text-gray-600">Portfolio ID: {{ portfolio.portfolio_id }}</p>
        </div>
      </div>
      <button @click="fetchPortfolios" class="border bg-black p-4 text-white">Click Here to Refresh Portfolios</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        portfolios: []
      };
    },
    methods: {
      fetchPortfolios() {
        axios.get('http://127.0.0.1:8000/get-all-portfolios/')
          .then(response => {
            this.portfolios = response.data.portfolios;
          })
          .catch(error => {
            console.error('Error:', error);
          });
      },
      selectPortfolio(portfolio) {
        this.$emit('portfolio-selected', portfolio); // Emit an event with the selected portfolio
      }
    }
  };
  </script>