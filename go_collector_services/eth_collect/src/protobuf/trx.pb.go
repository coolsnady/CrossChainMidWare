// Code generated by protoc-gen-go. DO NOT EDIT.
// source: trx.proto

package protobuf

import proto "github.com/golang/protobuf/proto"
import fmt "fmt"
import math "math"

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion2 // please upgrade the proto package

type TrxObject struct {
	BlockNumber          *int32   `protobuf:"varint,1,req,name=BlockNumber" json:"BlockNumber,omitempty"`
	From                 *string  `protobuf:"bytes,2,req,name=from" json:"from,omitempty"`
	To                   *string  `protobuf:"bytes,3,req,name=to" json:"to,omitempty"`
	Gas                  *int32   `protobuf:"varint,4,req,name=gas" json:"gas,omitempty"`
	Gasprice             *string  `protobuf:"bytes,5,req,name=gasprice" json:"gasprice,omitempty"`
	Input                *string  `protobuf:"bytes,6,req,name=input" json:"input,omitempty"`
	Nonce                *int32   `protobuf:"varint,7,req,name=nonce" json:"nonce,omitempty"`
	TransactionIndex     *int32   `protobuf:"varint,8,req,name=transactionIndex" json:"transactionIndex,omitempty"`
	Value                *string  `protobuf:"bytes,9,req,name=value" json:"value,omitempty"`
	ContractAddress      *string  `protobuf:"bytes,10,req,name=contractAddress" json:"contractAddress,omitempty"`
	GasUsed              *int32   `protobuf:"varint,11,req,name=gasUsed" json:"gasUsed,omitempty"`
	Status               *bool    `protobuf:"varint,12,req,name=status" json:"status,omitempty"`
	Logs                 *string  `protobuf:"bytes,13,req,name=logs" json:"logs,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *TrxObject) Reset()         { *m = TrxObject{} }
func (m *TrxObject) String() string { return proto.CompactTextString(m) }
func (*TrxObject) ProtoMessage()    {}
func (*TrxObject) Descriptor() ([]byte, []int) {
	return fileDescriptor_trx_121fdfa7513ae922, []int{0}
}
func (m *TrxObject) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_TrxObject.Unmarshal(m, b)
}
func (m *TrxObject) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_TrxObject.Marshal(b, m, deterministic)
}
func (dst *TrxObject) XXX_Merge(src proto.Message) {
	xxx_messageInfo_TrxObject.Merge(dst, src)
}
func (m *TrxObject) XXX_Size() int {
	return xxx_messageInfo_TrxObject.Size(m)
}
func (m *TrxObject) XXX_DiscardUnknown() {
	xxx_messageInfo_TrxObject.DiscardUnknown(m)
}

var xxx_messageInfo_TrxObject proto.InternalMessageInfo

func (m *TrxObject) GetBlockNumber() int32 {
	if m != nil && m.BlockNumber != nil {
		return *m.BlockNumber
	}
	return 0
}

func (m *TrxObject) GetFrom() string {
	if m != nil && m.From != nil {
		return *m.From
	}
	return ""
}

func (m *TrxObject) GetTo() string {
	if m != nil && m.To != nil {
		return *m.To
	}
	return ""
}

func (m *TrxObject) GetGas() int32 {
	if m != nil && m.Gas != nil {
		return *m.Gas
	}
	return 0
}

func (m *TrxObject) GetGasprice() string {
	if m != nil && m.Gasprice != nil {
		return *m.Gasprice
	}
	return ""
}

func (m *TrxObject) GetInput() string {
	if m != nil && m.Input != nil {
		return *m.Input
	}
	return ""
}

func (m *TrxObject) GetNonce() int32 {
	if m != nil && m.Nonce != nil {
		return *m.Nonce
	}
	return 0
}

func (m *TrxObject) GetTransactionIndex() int32 {
	if m != nil && m.TransactionIndex != nil {
		return *m.TransactionIndex
	}
	return 0
}

func (m *TrxObject) GetValue() string {
	if m != nil && m.Value != nil {
		return *m.Value
	}
	return ""
}

func (m *TrxObject) GetContractAddress() string {
	if m != nil && m.ContractAddress != nil {
		return *m.ContractAddress
	}
	return ""
}

func (m *TrxObject) GetGasUsed() int32 {
	if m != nil && m.GasUsed != nil {
		return *m.GasUsed
	}
	return 0
}

func (m *TrxObject) GetStatus() bool {
	if m != nil && m.Status != nil {
		return *m.Status
	}
	return false
}

func (m *TrxObject) GetLogs() string {
	if m != nil && m.Logs != nil {
		return *m.Logs
	}
	return ""
}

func init() {
	proto.RegisterType((*TrxObject)(nil), "tutorial.TrxObject")
}

func init() { proto.RegisterFile("trx.proto", fileDescriptor_trx_121fdfa7513ae922) }

var fileDescriptor_trx_121fdfa7513ae922 = []byte{
	// 256 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0x64, 0x90, 0xcb, 0x4a, 0xc5, 0x30,
	0x10, 0x86, 0x31, 0xe7, 0xd6, 0xce, 0xf1, 0x72, 0x18, 0x44, 0x06, 0x57, 0xc5, 0x55, 0x71, 0xe1,
	0x3b, 0xe8, 0xce, 0x8d, 0x42, 0xd1, 0x07, 0xc8, 0x49, 0x63, 0xa9, 0xf6, 0x64, 0x4a, 0x32, 0x95,
	0xbe, 0xac, 0xef, 0x22, 0x9d, 0xaa, 0x88, 0xee, 0xfe, 0xef, 0x9b, 0xc9, 0x1f, 0x18, 0xc8, 0x25,
	0x8e, 0x37, 0x7d, 0x64, 0x61, 0xcc, 0x64, 0x10, 0x8e, 0xad, 0xed, 0xae, 0x3e, 0x0c, 0xe4, 0x4f,
	0x71, 0x7c, 0xdc, 0xbf, 0x7a, 0x27, 0x58, 0xc0, 0xf6, 0xae, 0x63, 0xf7, 0xf6, 0x30, 0x1c, 0xf6,
	0x3e, 0xd2, 0x51, 0x61, 0xca, 0x55, 0xf5, 0x5b, 0x21, 0xc2, 0xf2, 0x25, 0xf2, 0x81, 0x4c, 0x61,
	0xca, 0xbc, 0xd2, 0x8c, 0xa7, 0x60, 0x84, 0x69, 0xa1, 0xc6, 0x08, 0xe3, 0x0e, 0x16, 0x8d, 0x4d,
	0xb4, 0xd4, 0xd7, 0x53, 0xc4, 0x4b, 0xc8, 0x1a, 0x9b, 0xfa, 0xd8, 0x3a, 0x4f, 0x2b, 0xdd, 0xfb,
	0x61, 0x3c, 0x87, 0x55, 0x1b, 0xfa, 0x41, 0x68, 0xad, 0x83, 0x19, 0x26, 0x1b, 0x38, 0x38, 0x4f,
	0x1b, 0x6d, 0x99, 0x01, 0xaf, 0x61, 0x27, 0xd1, 0x86, 0x64, 0x9d, 0xb4, 0x1c, 0xee, 0x43, 0xed,
	0x47, 0xca, 0x74, 0xe1, 0x9f, 0x9f, 0x1a, 0xde, 0x6d, 0x37, 0x78, 0xca, 0xe7, 0x5e, 0x05, 0x2c,
	0xe1, 0xcc, 0x71, 0x90, 0x68, 0x9d, 0xdc, 0xd6, 0x75, 0xf4, 0x29, 0x11, 0xe8, 0xfc, 0xaf, 0x46,
	0x82, 0x4d, 0x63, 0xd3, 0x73, 0xf2, 0x35, 0x6d, 0xf5, 0x8b, 0x6f, 0xc4, 0x0b, 0x58, 0x27, 0xb1,
	0x32, 0x24, 0x3a, 0x2e, 0x4c, 0x99, 0x55, 0x5f, 0x34, 0xdd, 0xa6, 0xe3, 0x26, 0xd1, 0xc9, 0x7c,
	0x9b, 0x29, 0x7f, 0x06, 0x00, 0x00, 0xff, 0xff, 0xe0, 0x56, 0x0f, 0x7d, 0x75, 0x01, 0x00, 0x00,
}