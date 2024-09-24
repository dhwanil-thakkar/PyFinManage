<!-- Portfolios.vue -->

<template>
    <div id="PortfolioContainer" class="h-full flex flex-col">
      <h1 class="text-4xl font-bold mb-4 center">Portfolios</h1>
      <button @click="fetchPortfolios" class="border rounded-md bg-black mx-4 p-4 text-white">Refresh Portfolios</button>
      <div id="portfolios" class="flex-grow overflow-y-auto space-y-4 m-4 p-4">
        <div v-for="portfolio in portfolios" :key="portfolio.portfolio_id" 
             class="p-4 bg-white shadow-md rounded-md" @click="selectPortfolio(portfolio)">
          <h2 class="text-xl font-semibold">{{ portfolio.name }}</h2>
          <p class="text-gray-600">Portfolio ID: {{ portfolio.portfolio_id }}</p>
        </div>
      </div>
      <div>
        <AddNewPortfolio @portfolio-added="fetchPortfolios" class="shadow-md bg-white" />
      </div>
    </div>
  </template>
  
<script>
  import axios from 'axios';
  import { API_APP_URL } from '@/config';
  import AddNewPortfolio from './AddNewPortfolio.vue';
  
  export default {
    components :{
      AddNewPortfolio,
    },
    data() {
      return {
        portfolios: [],
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