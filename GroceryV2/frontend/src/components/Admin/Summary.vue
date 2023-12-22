<template>
    <div>
      <AdminNav v-if="isAdmin"/>
      <div v-if="summaryData.length > 0 && isAdmin">
        <div v-for="(venueData, index) in summaryData" :key="index" class="venue-summary">          
          <div>
            <hr/>
          </div>
          <div class="chart-container">
            <img :src="chartImages[index]" alt="Chart" class="chart-image" />
          </div>
        </div>
      </div>
      <div v-else>
        <h1>You need to login as an Admin to access this page.</h1>
      </div>
    </div>
  </template>
  
  <style>
  .venue-summary {
    margin-bottom: 0px; 
  }
  
  .chart-container {
    margin-top: 100px;
    margin-bottom: 20px; 
    display: list-item;
    justify-content: center;
  }
  
  .chart-image {
    max-width: 80%;
    height: auto;
    border: 1px solid #b16868;
    padding:  auto;
  }
  </style>
  
  
  
  <script>
  import AdminNav from './AdminNav.vue';
  import axios from 'axios';
  
  export default {
    name: 'Summary',
    components: {
      AdminNav,
    },
    data() {
      return {
        summaryData: [],
        chartImages: [],
        isAdmin:false
      };
    },
    created() {
      this.fetchSummaryData();
    },
    methods: {
      fetchSummaryData() {
        axios
          .get('http://127.0.0.1:5000/api/admin/summary', {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') },
          })
          .then(response => {
            this.summaryData = response.data.summary_data;
            this.chartImages = response.data.chart_images;
            this.isAdmin=true;
          })
          .catch(error => {
            console.error(error);
            this.isAdmin=false;
          });
      },
    },
  };
  </script>
  
