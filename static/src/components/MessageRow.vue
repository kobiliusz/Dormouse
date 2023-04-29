<template>

<div>
    <span class="msg-header">
        {{ getFormattedDate() }} | {{ nick }}
    </span>
    <span class="msg-content">
        {{ content }}
    </span>
</div>

</template>
<script>

export default {
    props: {
        content: String,
        nick: String,
        timestamp: Number
    },

    methods: {
        getFormattedDate() {
            const date = new Date(this.timestamp)
            const hours = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0')
            const seconds = date.getSeconds().toString().padStart(2, '0')
            return `${hours}:${minutes}:${seconds}`
        }
    }

}

</script>
<style>

</style>