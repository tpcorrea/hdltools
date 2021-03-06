---------------------------------------------------------------------------------------------------------
-- This code and it autogenerated outputs are provided under LGPL by Ricardo Tafas.                    --
-- What does that mean? That you get it for free as long as you give back all good stiff you add to it.--
-- You can download more VHDL stuff at https://github.com/rftafas                                      --
---------------------------------------------------------------------------------------------------------
library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;

entity axis_custom is
    generic (
      tdata_size   : integer := 8;
      tdest_size   : integer := 8;
      tuser_size   : integer := 8
    );
    port (
      clk_i       : in  std_logic;
      rst_i       : in  std_logic;
      --python port code
      --Custom ports go here.
      example_port : in  std_logic
    );
end axis_custom;

architecture behavioral of axis_custom is

--python constant code

  constant all1_c : std_logic_vector(number_ports-1 downto 0) := (others=>'1');

  type axi_tdata_array is array (natural range <>) of std_logic_vector(tdata_size-1 downto 0);
  type axi_tuser_array is array (natural range <>) of std_logic_vector(tuser_size-1 downto 0);
  type axi_tdest_array is array (natural range <>) of std_logic_vector(tdest_size-1 downto 0);

  signal s_tdata_s  :  axi_tdata_array(number_slaves-1 downto 0);
  signal s_tuser_s  :  axi_tuser_array(number_slaves-1 downto 0);
  signal s_tdest_s  :  axi_tdest_array(number_slaves-1 downto 0);
  signal s_tvalid_s : std_logic_vector(number_slaves-1 downto 0);
  signal s_tlast_s  : std_logic_vector(number_slaves-1 downto 0);
  signal s_tready_s : std_logic_vector(number_slaves-1 downto 0);

  signal m_tdata_s  :  axi_tdata_array(number_masters-1 downto 0);
  signal m_tuser_s  :  axi_tuser_array(number_masters-1 downto 0);
  signal m_tdest_s  :  axi_tdest_array(number_masters-1 downto 0);
  signal m_tvalid_s : std_logic_vector(number_masters-1 downto 0);
  signal m_tlast_s  : std_logic_vector(number_masters-1 downto 0);
  signal m_tready_s : std_logic_vector(number_masters-1 downto 0);

  --your custom signals go here.

begin

--python signal connections

-- your code goes here.
-- Make sure to use the following signals instead the ports:
-- s_tdata_s
-- s_tuser_s
-- s_tdest_s
-- s_tvalid_s
-- s_tlast_s
-- s_tready_s
-- m_tdata_s
-- m_tuser_s
-- m_tdest_s
-- m_tvalid_s
-- m_tlast_s
-- m_tready_s

end behavioral;
