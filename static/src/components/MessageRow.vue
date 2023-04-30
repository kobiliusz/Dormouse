<template>

<div class="msg">
    <span class="msg-header">
        {{ getFormattedDate() }} | {{ nick }}
    </span>
    <span class="msg-content" v-html="content">
        
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
            const date = new Date(this.timestamp*1000)
            const hours = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0')
            const seconds = date.getSeconds().toString().padStart(2, '0')
            return `${hours}:${minutes}:${seconds}`
        }
    }

}

</script>
<style>
    .msg-header {
        font-weight: bold;
        margin-right: 7px;
    }
    .msg {
        padding-bottom: 7px;
    }
    a {
        text-decoration: none;
        color: #d79a00;
    }
    a:hover {
        text-decoration: underline;
    }

</style>