`define CHIP_TOP        chip_7nm_top
`define PERIPH1_WRAP    `CHIP_TOP.u_periph1_wrapper
`define PERIPH2_WRAP    `CHIP_TOP.u_periph2_wrapper
`define UART1_INST      `PERIPH1_WRAP.u_uart1_inst
`define UART1_REGS      `UART1_INST.reg_block
`define DMA_INST        `PERIPH2_WRAP.u_dma_inst
`define DMA_CHAN0       `DMA_INST.channel[0]
