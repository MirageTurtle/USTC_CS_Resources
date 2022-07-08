`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: USTC ESLAB
// Engineer: Huang Yifan (hyf15@mail.ustc.edu.cn)
// 
// Design Name: RV32I Core
// Module Name: Hazard Module
// Tool Versions: Vivado 2017.4.1
// Description: Hazard Module is used to control flush, bubble and bypass
// 
//////////////////////////////////////////////////////////////////////////////////

//  鍔熻兘璇存槑
    //  璇嗗埆娴佹按绾夸腑鐨勬暟鎹啿绐侊紝鎺у埗鏁版嵁杞彂锛屽拰flush銆乥ubble淇″彿
// 杈撳叆
    // rst               CPU鐨剅st淇″彿
    // reg1_srcD         ID闃舵鐨勬簮reg1鍦板潃
    // reg2_srcD         ID闃舵鐨勬簮reg2鍦板潃
    // reg1_srcE         EX闃舵鐨勬簮reg1鍦板潃
    // reg2_srcE         EX闃舵鐨勬簮reg2鍦板潃
    // reg_dstE          EX闃舵鐨勭洰鐨剅eg鍦板潃
    // reg_dstM          MEM闃舵鐨勭洰鐨剅eg鍦板潃
    // reg_dstW          WB闃舵鐨勭洰鐨剅eg鍦板潃
    // br                鏄惁branch
    // jalr              鏄惁jalr
    // jal               鏄惁jal
    // wb_select         锟斤拷锟斤拷EX锟轿碉拷WBselect锟斤拷锟叫讹拷ex指锟斤拷锟角凤拷为load指锟斤拷
    // reg_write_en_MEM  MEM闃舵鐨勫瘎瀛樺櫒鍐欎娇鑳戒俊锟�?
    // reg_write_en_WB   WB闃舵鐨勫瘎瀛樺櫒鍐欎娇鑳戒俊锟�?
// 杈撳嚭
    // flushF            IF闃舵鐨刦lush淇″彿
    // bubbleF           IF闃舵鐨刡ubble淇″彿
    // flushD            ID闃舵鐨刦lush淇″彿
    // bubbleD           ID闃舵鐨刡ubble淇″彿
    // flushE            EX闃舵鐨刦lush淇″彿
    // bubbleE           EX闃舵鐨刡ubble淇″彿
    // flushM            MEM闃舵鐨刦lush淇″彿
    // bubbleM           MEM闃舵鐨刡ubble淇″彿
    // flushW            WB闃舵鐨刦lush淇″彿
    // bubbleW           WB闃舵鐨刡ubble淇″彿
    // op1_sel           00 is reg1, 01 is mem stage forwarding, 01 is wb stage forwarding
    // op2_sel           00 is reg2, 01 is mem stage forwarding, 01 is wb stage forwarding


`include "Parameters.v"   
module HarzardUnit(
    input wire rst,
    input wire [4:0] reg1_srcD, reg2_srcD, reg1_srcE, reg2_srcE, reg_dstE, reg_dstM, reg_dstW,
    input wire br, jalr, jal,
    input wire wb_select,
    input wire reg_write_en_MEM,
    input wire reg_write_en_WB,
    output reg flushF, bubbleF, flushD, bubbleD, flushE, bubbleE, flushM, bubbleM, flushW, bubbleW,
    output reg [1:0] op1_sel, op2_sel
    );

    // TODO: Complete this module
    // generate op1_sel
    always @ (*)
    begin 
        if (reg1_srcE == reg_dstM && reg_write_en_MEM == 1 && reg1_srcE != 0)
        begin
            // mem to ex forwarding, mem forwarding first
            op1_sel = 2'b01;
        end
        else if (reg1_srcE == reg_dstW && reg_write_en_WB == 1 && reg1_srcE != 0)
        begin
            // wb to ex forwarding
            op1_sel = 2'b10;
        end
        else 
        begin
            op1_sel = 2'b00;
        end
    end
    
    // generate op2_sel
    always @ (*)
    begin
        if (reg2_srcE == reg_dstM && reg_write_en_MEM == 1 && reg2_srcE != 0)
        begin
            // mem to ex forwarding, mem forwarding first
            op2_sel = 2'b01;
        end
        else if (reg2_srcE == reg_dstW && reg_write_en_WB == 1 && reg2_srcE != 0)
        begin
            // wb to ex forwarding
            op2_sel = 2'b10;
        end
        else 
        begin
            op2_sel = 2'b00;
        end
    end
    
    // generate bubbleF and flushF and bubbleD and flushD and  bubbleE and flushE
    always @ (*)
    begin
        if (rst)
        begin
            bubbleF = 0;
            flushF = 1;
            bubbleD = 0;
            flushD = 1;
            bubbleE = 0;
            flushD = 1;
        end
        else 
        begin
            if (wb_select == 1 && (reg_dstE == reg1_srcD || reg_dstE == reg2_srcD))
            begin
                // load-use type data hazard, bubble IF, bubble ID, flush EX 
                bubbleF = 1;
                flushF = 0;
                bubbleD = 1;
                flushD = 0;
                bubbleE = 0;
                flushE = 1;
            end
            // implement branch predict with default no branch
            else if (br == 1)
            begin
                // branch instruction, flush ID, 
                bubbleF = 0;
                flushF = 0;
                bubbleD = 0;
                flushD = 1;
                bubbleE = 0;
                flushE = 1;
            end
            else if (jalr == 1)
            begin
                bubbleF = 0;
                flushF = 0;
                bubbleD = 0;
                flushD = 1;
                bubbleE = 0;
                flushE = 1;
            end
            else if (jal == 1)
            begin
                bubbleF = 0;
                flushF = 0;
                bubbleD = 0;
                flushD = 1;
                bubbleE = 0;
                flushE = 0;
            end
            else
            begin
                bubbleF = 0;
                flushF = 0;
                bubbleD = 0;
                flushD = 0;
                bubbleE = 0;
                flushE = 0;
            end
        end
    end
    
    // generate bubbleM and flushM
    always @ (*)
    begin
        if (rst)
        begin
            bubbleM = 0;
            flushM = 1;
        end
        else 
        begin
            bubbleM = 0;
            flushM = 0;
        end
    end
    
    
    // generate bubbleW and flushW
    always @ (*)
    begin
        if (rst)
        begin
            bubbleW = 0;
            flushW = 1;
        end
        else 
        begin
            bubbleW = 0;
            flushW = 0;
        end
    end

endmodule