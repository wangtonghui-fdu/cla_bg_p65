// P65 CLA BG trace snippet for c2000_tb.v
//
// 用法：
// 1. 备份服务器工程里的 fpga/c2000_tb.v。
// 2. 将本片段插入 c2000_tb.v 的 module 内部、endmodule 之前。
// 3. 如果原 TB 已经定义了同名 integer 或 wire，只保留一份，避免重复定义。
// 4. 重新执行 source sourceme && make comp_fullchip。

`ifndef P65_CLA_BG_TRACE_SNIPPET_V
`define P65_CLA_BG_TRACE_SNIPPET_V

initial begin
  $timeformat(-9, 0, " ns", 10);
end

integer fp_cla_gr_bgtask;
integer fp_cla_bg_pc;
integer fp_cla_bg_state;
integer fp_cla_bg_irq;
integer fp_cla_bg_timeline;

initial begin
  fp_cla_gr_bgtask  = $fopen("cla_bgtask_sprs_trace.dat", "w");
  fp_cla_bg_pc      = $fopen("cla_bgtask_pc_trace.dat", "w");
  fp_cla_bg_state   = $fopen("cla_bgtask_state_trace.dat", "w");
  fp_cla_bg_irq     = $fopen("cla_bgtask_irq_trace.dat", "w");
  fp_cla_bg_timeline= $fopen("cla_bgtask_timeline_trace.dat", "w");
end

// CLA RFGR write-back signals.
wire [31:0] cla_rfgr_din_s0_core_0  = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.din_s0[31:0];
wire [31:0] cla_rfgr_din1_s0_core_0 = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.din_s2[31:0];
wire [31:0] cla_rfgr_din_s1_core_0  = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.din_s1[31:0];
wire [31:0] cla_rfgr_dinx_s1_core_0 = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.dinx_s1[31:0];
wire [31:0] cla_rfgr_dinx_s2_core_0 = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.dinx_s2[31:0];

wire cla_rfgr_wen_s0  = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.wen_s0;
wire cla_rfgr_wen_s2  = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.wen_s2;
wire cla_rfgr_wen_s1  = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.wen_s1;
wire cla_rfgr_wenx_s1 = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.wenx_s1;
wire cla_rfgr_wenx_s2 = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.wenx_s2;

wire cla_clk = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.clk;
wire cla_rst = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.rst;

wire [4:0] cla_rfgr_waddr_s0  = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.waddr_s0[4:0];
wire [4:0] cla_rfgr_waddr_s2  = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.waddr_s2[4:0];
wire [4:0] cla_rfgr_waddr_s1  = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.waddr_s1[4:0];
wire [4:0] cla_rfgr_waddrx_s1 = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.waddrx_s1[4:0];
wire [4:0] cla_rfgr_waddrx_s2 = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.rfgr.waddrx_s2[4:0];

wire bgtask_run = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_task.task8_run;
wire [31:0] me3_current_pc = tb.dsp_c2000.u_c2000_digital.cpu_top_u.cpu0.cla.cla_scale.cla_m3_scale.me3_current_pc[31:0];

reg bgtask_run_d;
reg [31:0] me3_current_pc_d;

always @(negedge cla_clk) begin
  if (cla_rst) begin
    if (bgtask_run !== bgtask_run_d) begin
      $fwrite(fp_cla_bg_timeline, "BG_RUN\t%b->%b\tPC=0x%h\t[%0t]\n", bgtask_run_d, bgtask_run, me3_current_pc, $time);
      $fwrite(fp_cla_bg_state, "BG_RUN\t0x%h\t%b\t[%0t]\n", me3_current_pc, bgtask_run, $time);
      $fflush(fp_cla_bg_timeline);
      $fflush(fp_cla_bg_state);
    end

    if (me3_current_pc !== me3_current_pc_d) begin
      $fwrite(fp_cla_bg_pc, "PC\t0x%h\tRUN=%b\t[%0t]\n", me3_current_pc, bgtask_run, $time);
      $fflush(fp_cla_bg_pc);
    end

    // 只记录 task8 地址空间的 GR 写回。P65 BG task8 常见起始地址在 0x4d8 附近。
    if (me3_current_pc >= 'h4d8) begin
      if (cla_rfgr_wen_s0)
        $fwrite(fp_cla_gr_bgtask, "0x%h\t0x%h\t0x%h\t[%0t]\n", cla_rfgr_waddr_s0, cla_rfgr_din_s0_core_0, me3_current_pc, $time);
      if (cla_rfgr_wen_s2)
        $fwrite(fp_cla_gr_bgtask, "0x%h\t0x%h\t0x%h\t[%0t]\n", cla_rfgr_waddr_s2, cla_rfgr_din1_s0_core_0, me3_current_pc, $time);
      if (cla_rfgr_wen_s1)
        $fwrite(fp_cla_gr_bgtask, "0x%h\t0x%h\t0x%h\t[%0t]\n", cla_rfgr_waddr_s1, cla_rfgr_din_s1_core_0, me3_current_pc, $time);
      if (cla_rfgr_wenx_s1)
        $fwrite(fp_cla_gr_bgtask, "0x%h\t0x%h\t0x%h\t[%0t]\n", cla_rfgr_waddrx_s1, cla_rfgr_dinx_s1_core_0, me3_current_pc, $time);
      if (cla_rfgr_wenx_s2)
        $fwrite(fp_cla_gr_bgtask, "0x%h\t0x%h\t0x%h\t[%0t]\n", cla_rfgr_waddrx_s2, cla_rfgr_dinx_s2_core_0, me3_current_pc, $time);
      $fflush(fp_cla_gr_bgtask);
    end
  end

  bgtask_run_d <= bgtask_run;
  me3_current_pc_d <= me3_current_pc;
end

`endif
