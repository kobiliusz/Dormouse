<template>
  <div>
    <label for="room-list">Room</label>
    <select @change="selectRoom($event)" name="room-list" id="room-list">
      <option v-for="room in rooms" :key="room.id">{{ room.name }}</option>
    </select>
  </div>
</template>

<script>
import axios from "axios";
export default {
  
  data() {
    return {
      rooms: [],
      room_id: 1
    }
  },
  
  methods: {
    getRooms() {
      axios.get('http://localhost:80/api/rooms')
        .then(response => {
          this.rooms = response.data
        }).catch(error => {
          console.log(error)
        })
    },
    selectRoom(event) {
      this.room_id = event.target.key
    }
  },

  mounted() {
    this.getRooms()
  }

}
</script>

<style>

</style>
