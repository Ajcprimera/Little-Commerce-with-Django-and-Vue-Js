<script setup>
import { ref, onMounted } from 'vue';
import $ from 'jquery';
import 'datatables.net';
import 'datatables.net-dt/css/dataTables.dataTables.css';
import apiClient from '../api/api.js';
import EditarIcon from '../assets/editar.svg';
import EliminarIcon from '../assets/eliminar.svg';
import ReviewIcon from '../assets/review.svg';
import VerIcon from '../assets/ver.svg';

const products = ref([]);
const table = ref(null);
const emit = defineEmits(['view-product']);


const fetchProducts = async () => {
  try {
    const response = await apiClient.get('/products/');
    products.value = response.data;
    initializeDataTable();
  } catch (error) {
    console.error('Error al cargar los productos:', error);
  }
};

const deleteProduct = async (id) => {
  try {
    await apiClient.delete(`/products/${id}/`);
    alert(`Producto con ID ${id} eliminado exitosamente.`);
    fetchProducts(); // Recarga los datos para reflejar los cambios
  } catch (error) {
    console.error(`Error al eliminar el producto con ID ${id}:`, error);
    alert('No se pudo eliminar el producto. Inténtalo de nuevo.');
  }
};


const initializeDataTable = () => {
  if (table.value) {
    $(table.value).DataTable({
      data: products.value,
      columns: [
        { data: 'title', title: 'Nombre' },
        { data: 'description', title: 'Descripción' },
        { data: 'price', title: 'Precio' },
        { 
          data: null, 
          title: 'Acciones', 
          orderable: false, 
          render: (data, type, row) => {
            return `
              <button class="edit-btn" data-id="${row.id}"><img src="${EditarIcon}" alt="Editar" class="size-6"></button>
              <button class="view-btn" data-id="${row.id}"><img src="${VerIcon}" alt="Ver" class="size-6"></button>
              <button class="delete-btn" data-id="${row.id}"><img src="${EliminarIcon}" alt="Editar" class="size-6"></button>
              <button class="review-btn" data-id="${row.id}"><img src="${ReviewIcon}" alt="Review" class="size-6"></button>
            `;
          } 
        },
      ],
      columnDefs: [
        { width: '350px', targets: 3 }
      ],
      destroy: true,
      responsive: true,
      drawCallback: function() {
        $('.delete-btn').off('click').on('click', function() {
          const productId = $(this).data('id');
          deleteProduct(productId);
        });
        $('.view-btn').off('click').on('click', function() {
          const productId = $(this).data('id');
          const product = products.value.find(p => p.id === productId);
          emit('view-product', product); // Emitimos el evento al padre
        });
        // Dentro de drawCallback
        $('.edit-btn').off('click').on('click', function() {
          const productId = $(this).data('id');
          const product = products.value.find(p => p.id === productId);
          emit('edit-product', product); // Emitimos el evento al padre
        });
        $('.review-btn').off('click').on('click', function() {
          const productId = $(this).data('id');
          const product = products.value.find(p => p.id === productId);
          emit('review-product', product); // Emitimos el evento al padre
        });
      },
    });
  }
};


onMounted(() => {
  fetchProducts();
});
</script>

<template>
  <div>
    <table ref="table" class="display" style="width:100%"></table>
  </div>
</template>

<style>

.display {
  width: 100%;
  margin: 20px 0;
}

table td .size-6 {
  width: 24px;
  height: 24px;
}

table td button {
  margin: 0 2px;
  padding: 8px;
}
</style>