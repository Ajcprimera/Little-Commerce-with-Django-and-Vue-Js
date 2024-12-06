<!-- src/App.vue -->
<script setup>
import { nextTick } from 'vue';
import { ref, onMounted, watch } from 'vue'
import Modal from './components/Modal.vue'
import Datatable from './components/Datatable.vue';
import apiClient from './api/api.js'
import Multiselect from 'vue-multiselect'
import JsBarcode from 'jsbarcode'
import QRCode from 'qrcode'

const value = ref([])
const options = ref([])

const showEditModal = ref(false);
const showReviewModal = ref(false);

const selectedProduct = ref(null);

const barcode = ref('')
const sku = ref('')
const thumbnail = ref('')
const qrCode = ref('')
const title = ref('')
const description = ref('')
const category = ref('')
const price = ref(null)
const discountPercentage = ref(null)
const rating = ref(null)
const stock = ref(null)
const minimumOrderQuantity = ref(null)
const warrantyInformation = ref('')
const shippingInformation = ref('')
const availabilityStatus = ref('')
const returnPolicy = ref('')
const images = ref([])
const width = ref(null)
const height = ref(null)
const depth = ref(null)
const brand = ref('')
const weight = ref(null)

const showCreateModal = ref(false);
const showDetailModal = ref(false);

const reviewRating = ref(null);
const reviewComment = ref('');
const reviewerName = ref('');
const reviewerEmail = ref('');

const reviews = ref([]); 
const hasLoadedReviews = ref(false);

const openReviewModal = (product) => {
  selectedProduct.value = product;
  showReviewModal.value = true;
};

const openModal = () => {
  showCreateModal.value = true;
}

const openEditModal = (product) => {
  selectedProduct.value = product;
  showEditModal.value = true;
  title.value = product.title;
  description.value = product.description;
  category.value = product.category;
  price.value = product.price;
  discountPercentage.value = product.discount_percentage;
  rating.value = product.rating;
  stock.value = product.stock;
  brand.value = product.brand;
  weight.value = product.weight;
  minimumOrderQuantity.value = product.minimum_order_quantity;
  sku.value = product.sku;
  warrantyInformation.value = product.warranty_information;
  shippingInformation.value = product.shipping_information;
  availabilityStatus.value = product.availability_status;
  returnPolicy.value = product.return_policy;
  images.value = product.images.join(', ');
  thumbnail.value = product.thumbnail;
  width.value = product.width;
  height.value = product.height;
  depth.value = product.depth;
  barcode.value = product.barcode;
  qrCode.value = product.qr_code;
  value.value = product.tags.map(tag => ({ name: tag.name, code: tag.id.toString() }));
};

const closeModal = () => {
  showCreateModal.value = false;
  showDetailModal.value = false;
  showEditModal.value = false;
  showReviewModal.value = false;
}

const openProductModal = async (product) => {
  selectedProduct.value = product;
  showDetailModal.value = true;
  reviews.value = []; // Limpiar reseñas al abrir el modal
  hasLoadedReviews.value = false; // Reiniciar el estado de carga de reseñas
  
  await nextTick();

  if (selectedProduct.value && selectedProduct.value.barcode) {
    JsBarcode("#barcode", selectedProduct.value.barcode.toString());
  } else {
    console.warn("No hay un código de barras válido para mostrar.");
  }

  if (selectedProduct.value && selectedProduct.value.qr_code) {
    const qrCodeElement = document.getElementById("qrcode");
    QRCode.toString(selectedProduct.value.qr_code, { type: 'svg', width: 128 }, function (error, svg) {
      if (error) console.error(error);
      qrCodeElement.innerHTML = svg;
    });
  } else {
    console.warn("No hay un código QR válido para mostrar.");
  }
};


const validateBarcode = () => {
  const barcodeStr = barcode.value?.toString().padStart(13, '0') || '';
  if (barcodeStr.length !== 13) {
    console.warn("El código de barras no tiene exactamente 13 dígitos.");
    alert('El código de barra debe tener exactamente 13 dígitos.');
    return false;
  }

  console.log("El código de barras es válido.");
  return true;
};

const validateSku = () => {
  if (sku.value.length !== 8) {
    alert('El SKU debe tener exactamente 8 caracteres.')
    return false
  }
  return true
}

const loadReviews = async (productId) => {
  hasLoadedReviews.value = true; // Marcar que se ha intentado cargar reseñas
  try {
    const response = await apiClient.get(`/products/${productId}/reviews/`);
    reviews.value = response.data; // Asignar las reseñas a la variable
  } catch (error) {
    console.error('Error al cargar las reseñas:', error);
    alert('Ocurrió un error al cargar las reseñas.');
  }
};

const updateProductRating = async (productId) => {
  try {
    const response = await apiClient.get(`/products/${productId}/reviews/`);
    const reviews = response.data;
    const averageRating = reviews.reduce((sum, review) => sum + review.rating, 0) / reviews.length;

    await apiClient.patch(`/products/${productId}/`, { rating: averageRating });
    console.log('Rating del producto actualizado:', averageRating);
  } catch (error) {
    console.error('Error al actualizar el rating del producto:', error);
  }
};


const loadTags = async () => {
  try {
    const response = await apiClient.get('/tags/');
    options.value = response.data.map(tag => ({
      name: tag.name,
      code: tag.id.toString()
    }));
  } catch (error) {
    console.error('Error al cargar las etiquetas:', error);
  }
};

onMounted(() => {
  loadTags();
});


const addTag = async (newTag) => {
  const existingTag = options.value.find(tag => tag.name === newTag);
  if (existingTag) {
    value.value.push(existingTag);
    return;
  }

  try {
    const response = await apiClient.post('/tags/', { name: newTag });
    const tag = {
      name: response.data.name,
      code: response.data.id.toString(),
    };
    options.value.push(tag);
    value.value.push(tag);
  } catch (error) {
    console.error('Error al crear la etiqueta:', error);
  }
};


const handleSubmit = async () => {
  const isBarcodeValid = validateBarcode()
  const isSkuValid = validateSku()

  if (isBarcodeValid && isSkuValid) {
    const productData = {
      title: title.value || '',
      description: description.value || '',
      category: category.value || '',
      price: parseFloat(price.value) || 0,
      discount_percentage: parseFloat(discountPercentage.value) || 0,
      rating: parseFloat(rating.value) || 0,
      stock: parseInt(stock.value, 10) || 0,
      tags: value.value.map(tag => ({ name: tag.name })),
      sku: sku.value || '',
      warranty_information: warrantyInformation.value || '',
      shipping_information: shippingInformation.value || '',
      availability_status: availabilityStatus.value || '',
      return_policy: returnPolicy.value || '',
      minimum_order_quantity: parseInt(minimumOrderQuantity.value, 10) || 1,
      images: images.value.length > 0
        ? images.value.split(',').map(url => url.trim())
        : [],
      thumbnail: thumbnail.value || '',
      width: parseFloat(width.value) || 0,
      height: parseFloat(height.value) || 0,
      depth: parseFloat(depth.value) || 0,
      barcode: parseInt(barcode.value, 10) || 0,
      qr_code: qrCode.value || '',
      brand: brand.value || '',
      weight: parseFloat(weight.value) || 0,
    };
    console.log('Datos del producto:', productData);
    try {
      const response = await apiClient.post('/products/', productData)
      console.log('Producto creado:', response.data)
      alert('Producto creado exitosamente.')
      closeModal()
      window.location.reload();
    } catch (error) {
      console.error('Error al crear el producto:', error)
      alert('Ocurrió un error al crear el producto.')
    }
  } else {
    console.error('Errores en el formulario')
  }
}

const handleReviewSubmit = async () => {
  const reviewData = {
    rating: reviewRating.value,
    comment: reviewComment.value,
    reviewer_name: reviewerName.value,
    reviewer_email: reviewerEmail.value,
    product: selectedProduct.value.id,
  };

  try {
    const response = await apiClient.post(`/products/${selectedProduct.value.id}/reviews/`, reviewData);
    console.log('Review creada:', response.data);
    alert('Review creada exitosamente.');
    closeModal();
    updateProductRating(selectedProduct.value.id);
    window.location.reload();
  } catch (error) {
    console.error('Error al crear la review:', error);
    alert('Ocurrió un error al crear la review.');
  }
};

const handleEditSubmit = async () => {
  const isBarcodeValid = validateBarcode();
  const isSkuValid = validateSku();

  if (isBarcodeValid && isSkuValid) {
    const productData = {
      title: title.value || '',
      description: description.value || '',
      category: category.value || '',
      price: parseFloat(price.value) || 0,
      discount_percentage: parseFloat(discountPercentage.value) || 0,
      rating: parseFloat(rating.value) || 0,
      stock: parseInt(stock.value, 10) || 0,
      tags: value.value.map(tag => ({ name: tag.name })),
      sku: sku.value || '',
      warranty_information: warrantyInformation.value || '',
      shipping_information: shippingInformation.value || '',
      availability_status: availabilityStatus.value || '',
      return_policy: returnPolicy.value || '',
      minimum_order_quantity: parseInt(minimumOrderQuantity.value, 10) || 1,
      images: images.value.length > 0
        ? images.value.split(',').map(url => url.trim())
        : [],
      thumbnail: thumbnail.value || '',
      width: parseFloat(width.value) || 0,
      height: parseFloat(height.value) || 0,
      depth: parseFloat(depth.value) || 0,
      barcode: parseInt(barcode.value, 10) || 0,
      qr_code: qrCode.value || '',
      brand: brand.value || '',
      weight: parseFloat(weight.value) || 0,
    };

    try {
      const response = await apiClient.put(`/products/${selectedProduct.value.id}/`, productData);
      console.log('Producto actualizado:', response.data);
      alert('Producto actualizado exitosamente.');
      closeModal();
      window.location.reload();
    } catch (error) {
      console.error('Error al actualizar el producto:', error);
      alert('Ocurrió un error al actualizar el producto.');
    }
  } else {
    console.error('Errores en el formulario');
  }
};

</script>

<template>
  <div class=" m-5">
    <h1 class="text-form">Manejador de productos</h1>
    <button @click="openModal">Crear un producto</button>
    <transition name="modal">
      <Modal v-if="showCreateModal" @close="closeModal">
        <form @submit.prevent="handleSubmit">
          <h2 class="text-form my-5">Informacion de producto</h2>
          <input class="input w-full m-1" placeholder="Nombre" type="text" v-model="title">
          <textarea class="input w-full m-1" placeholder="Descripcion" rows="2" v-model="description"></textarea>
          <multiselect 
            v-model="value" 
            tag-placeholder="Add this as new tag" 
            placeholder="Search or add a tag" 
            label="name"
            track-by="code" 
            :options="options" 
            :multiple="true" 
            :taggable="true" 
            @tag="addTag"
            class="m-1">
          </multiselect>
          <input class="input w-[31.9%] m-1" placeholder="Precio" type="number" step="0.01" v-model="price">
          <input class="input w-[31.9%] m-1" placeholder="Descuento" type="number" step="0.01" v-model="discountPercentage">
          <!--<input class="input w-[23.6%] m-1" placeholder="Puntuacion" type="number" step="0.1" v-model="rating">-->
          <input class="input w-[31.9%] m-1" placeholder="Stock" type="number" v-model="stock">
          <input class="input w-[31.9%] m-1" placeholder="Marca" type="text" v-model="brand">
          <input class="input w-[31.9%] m-1" placeholder="Peso" type="number" step="0.01" v-model="weight">
          <input class="input w-[31.9%] m-1" placeholder="Categoria" type="text" step="0.01" v-model="category">
          <input class="input w-[48.6%] m-1" placeholder="Cantidad minima de ordenes" type="number" v-model="minimumOrderQuantity">
          <input class="input w-[48.6%] m-1" placeholder="SKU" type="text" v-model="sku">
          <input class="input w-[48.6%] m-1" placeholder="Informacion de garantia" type="text" v-model="warrantyInformation">
          <input class="input w-[48.6%] m-1" placeholder="Informacion de envio" type="text" v-model="shippingInformation">
          <input class="input w-[48.6%] m-1" placeholder="Politica de retorno" type="text" v-model="returnPolicy">
          <input class="input w-[48.6%] m-1" placeholder="Estatus de disponibilidad" type="text" v-model="availabilityStatus">
          <input class="input w-[48.6%] m-1" placeholder="Imagenes" type="url" v-model="images">
          <input class="input w-[48.6%] m-1" placeholder="Miniatura" type="url" v-model="thumbnail">
          <h2 class="text-form my-0.5">Dimensiones</h2>
          <input class="input w-[31.9%] m-1" placeholder="Ancho" type="number" step="0.01" v-model="width">
          <input class="input w-[31.9%] m-1" placeholder="Alto" type="number" step="0.01" v-model="height">
          <input class="input w-[31.9%] m-1" placeholder="Profundidad" type="number" step="0.01" v-model="depth">
          <h2 class="text-form my-0.5">MetaInfo</h2>
          <input class="input w-[48.6%] m-1" placeholder="Código de barra" type="number" v-model="barcode">
          <input class="input w-[48.6%] m-1" placeholder="Código QR" type="url" v-model="qrCode">
          <div class="button-container">
            <button type="submit">Agregar</button>
          </div>
        </form>
      </Modal>
    </transition>

    <transition name="modal">
      <Modal v-if="showEditModal" @close="closeModal">
        <form @submit.prevent="handleEditSubmit">
          <h2 class="text-form my-5">Editar producto</h2>
          <!-- Formulario de edición de producto -->
          <input class="input w-full m-1" placeholder="Nombre" type="text" v-model="title">
          <textarea class="input w-full m-1" placeholder="Descripcion" rows="2" v-model="description"></textarea>
          <multiselect 
            v-model="value" 
            tag-placeholder="Add this as new tag" 
            placeholder="Search or add a tag" 
            label="name"
            track-by="code" 
            :options="options" 
            :multiple="true" 
            :taggable="true" 
            @tag="addTag"
            class="m-1">
          </multiselect>
          <input class="input w-[31.9%] m-1" placeholder="Precio" type="number" step="0.01" v-model="price">
          <input class="input w-[31.9%] m-1" placeholder="Descuento" type="number" step="0.01" v-model="discountPercentage">
          <!--<input class="input w-[23.6%] m-1" placeholder="Puntuacion" type="number" step="0.1" v-model="rating">-->
          <input class="input w-[31.9%] m-1" placeholder="Stock" type="number" v-model="stock">
          <input class="input w-[31.9%] m-1" placeholder="Marca" type="text" v-model="brand">
          <input class="input w-[31.9%] m-1" placeholder="Peso" type="number" step="0.01" v-model="weight">
          <input class="input w-[31.9%] m-1" placeholder="Categoria" type="text" step="0.01" v-model="category">
          <input class="input w-[48.6%] m-1" placeholder="Cantidad minima de ordenes" type="number" v-model="minimumOrderQuantity">
          <input class="input w-[48.6%] m-1" placeholder="SKU" type="text" v-model="sku">
          <input class="input w-[48.6%] m-1" placeholder="Informacion de garantia" type="text" v-model="warrantyInformation">
          <input class="input w-[48.6%] m-1" placeholder="Informacion de envio" type="text" v-model="shippingInformation">
          <input class="input w-[48.6%] m-1" placeholder="Politica de retorno" type="text" v-model="returnPolicy">
          <input class="input w-[48.6%] m-1" placeholder="Estatus de disponibilidad" type="text" v-model="availabilityStatus">
          <input class="input w-[48.6%] m-1" placeholder="Imagenes" type="url" v-model="images">
          <input class="input w-[48.6%] m-1" placeholder="Miniatura" type="url" v-model="thumbnail">
          <h2 class="text-form my-0.5">Dimensiones</h2>
          <input class="input w-[31.9%] m-1" placeholder="Ancho" type="number" step="0.01" v-model="width">
          <input class="input w-[31.9%] m-1" placeholder="Alto" type="number" step="0.01" v-model="height">
          <input class="input w-[31.9%] m-1" placeholder="Profundidad" type="number" step="0.01" v-model="depth">
          <h2 class="text-form my-0.5">MetaInfo</h2>
          <input class="input w-[48.6%] m-1" placeholder="Código de barra" type="number" v-model="barcode">
          <input class="input w-[48.6%] m-1" placeholder="Código QR" type="url" v-model="qrCode">
          <div class="button-container">
            <button type="submit">Actualizar</button>
          </div>
        </form>
      </Modal>
    </transition>

    <transition name="modal">
      <Modal v-if="showDetailModal" @close="closeModal">
        <div>
          <p><strong>Titulo:</strong> {{ selectedProduct?.title }}</p>
          <p><strong>Descripción:</strong> {{ selectedProduct?.description }}</p>
          <p><strong>Precio:</strong> {{ selectedProduct?.price }}</p>
          <p><strong>Descuento:</strong> {{ selectedProduct?.discount_percentage }}%</p>
          <p><strong>Puntuación:</strong> {{ selectedProduct?.rating }}</p>
          <p><strong>Stock:</strong> {{ selectedProduct?.stock }}</p>
          <p><strong>Categoría:</strong> {{ selectedProduct?.category }}</p>
          <p><strong>Marca:</strong> {{ selectedProduct?.brand }}</p>
          <p><strong>Peso:</strong> {{ selectedProduct?.weight }} kg</p>
          <p><strong>Cantidad mínima de orden:</strong> {{ selectedProduct?.minimum_order_quantity }}</p>
          <p><strong>SKU:</strong> {{ selectedProduct?.sku }}</p>
          <p><strong>Información de garantía:</strong> {{ selectedProduct?.warranty_information }}</p>
          <p><strong>Información de envío:</strong> {{ selectedProduct?.shipping_information }}</p>
          <p><strong>Política de retorno:</strong> {{ selectedProduct?.return_policy }}</p>
          <p><strong>Estatus de disponibilidad:</strong> {{ selectedProduct?.availability_status }}</p>
          <p><strong>Imágenes:</strong></p>
          <div id="imagesContainer" style="display: flex; flex-wrap: wrap; gap: 10px;">
            <img 
              v-for="(image, index) in selectedProduct?.images" 
              :key="index" 
              :src="image" 
              alt="Producto" 
              style="max-width: 200px; max-height: 200px;" 
              @error="onImageError"
            />
          </div>
          <p><strong>Miniatura:</strong></p>
          <img 
            v-if="selectedProduct?.thumbnail" 
            :src="selectedProduct.thumbnail" 
            alt="Miniatura del producto" 
            style="max-width: 200px; max-height: 200px;"
          />
          <p>Dimensiones:</p>
          <p><strong>Ancho:</strong> {{ selectedProduct?.width }} cm</p>
          <p><strong>Alto:</strong> {{ selectedProduct?.height }} cm</p>
          <p><strong>Profundidad:</strong> {{ selectedProduct?.depth }} cm</p>
          <p>MetaInfo:</p>
          <p><strong>Código de barra:</strong> </p>
          <svg id="barcode"></svg> 
          
          <p><strong>Código QR:</strong></p>
          <div id="qrcode"></div>
          <p><strong>Etiquetas:</strong></p>
          <ul>
            <li v-for="tag in selectedProduct?.tags" :key="tag.id">{{ tag.name }}</li>
          </ul>
          <div class="button-container">
            <button @click="loadReviews(selectedProduct.id)">Ver Reseñas</button>
          </div>
          
          <!-- Sección para mostrar las reseñas -->
          <div>
            <div v-if="hasLoadedReviews">
              <div v-if="reviews.length > 0">
                <ul>
                  <li v-for="review in reviews" :key="review.id">
                    <div class=" bg-green-300 p-2 rounded-md my-1">
                      <p><strong>Rating:</strong> {{ review.rating }}</p>
                      <p><strong>Comentario:</strong> {{ review.comment }}</p>
                      <p><strong>Nombre:</strong> {{ review.reviewer_name }}</p>
                      <p><strong>Email:</strong> {{ review.reviewer_email }}</p>
                    </div>
                  </li>
                </ul>
              </div>
              <div v-else>
                <p>No hay reseñas para este producto.</p>
              </div>
            </div>
          </div>
        </div>
      </Modal>
    </transition>

    <transition name="modal">
      <Modal v-if="showReviewModal" @close="closeModal">
        <form @submit.prevent="handleReviewSubmit">
          <h2 class="text-form my-5">Crear Review</h2>
          <input class="input w-full m-1" placeholder="Nombre del revisor" type="text" v-model="reviewerName">
          <input class="input w-full m-1" placeholder="Email del revisor" type="email" v-model="reviewerEmail">
          <input class="input w-full m-1" placeholder="Rating" type="number" step="1" v-model="reviewRating">
          <textarea class="input w-full m-1" placeholder="Comentario" rows="2" v-model="reviewComment"></textarea>
          <div class="button-container">
            <button type="submit">Crear Review</button>
          </div>
        </form>
      </Modal>
    </transition>

    <Datatable @view-product="openProductModal" @edit-product="openEditModal" @review-product="openReviewModal"/>
  </div>

</template>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
body {
  background-color: #ffffff; /* Gris claro */
  font-family: Arial, sans-serif;
  color: #000000; /* Color de texto oscuro para mejor contraste */
}

.text-form {
  font-size: 20px;
  font-weight: bold;
  color: #41b883;
  text-align: center;
}

.input {
  border: none;
  outline: none;
  border-radius: 15px;
  padding: 1em;
  background-color: #ccc;
  box-shadow: inset 2px 5px 10px rgba(0,0,0,0.3);
  transition: 300ms ease-in-out;
  font-size: 16px;
}

.input:focus {
  background-color: white;
  transform: scale(1.05);
  box-shadow: 13px 13px 100px #969696,
             -13px -13px 100px #ffffff;
}

.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.modal-enter-to, .modal-leave-from {
  opacity: 1;
  transform: scale(1);
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.button-container {
  display: flex;
  justify-content: center; 
}

button {
  position: relative;
  display: inline-block;
  margin: 15px;
  padding: 15px 30px;
  text-align: center;
  font-weight: bold;
  font-size: 18px;
  letter-spacing: 1px;
  text-decoration: none;
  color: #41b883;
  background: transparent;
  cursor: pointer;
  transition: ease-out 0.5s;
  border: 2px solid #41b883;
  border-radius: 10px;
  box-shadow: inset 0 0 0 0 #41b883;
}

button:hover {
  color: white;
  box-shadow: inset 0 -100px 0 0 #41b883;
}

button:active {
  transform: scale(0.9);
}

.multiselect__input {
  font-size: 16px !important; 
}
</style>