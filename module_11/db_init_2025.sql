/*
    Title: db_init_2025.sql
    Author: Tyler Moon
    Date: 24 Feburary 2025
    Description: winery database initialization script.
*/
CREATE DATABASE IF NOT EXISTS Winery;
USE Winery;
SET FOREIGN_KEY_CHECKS = 0;
-- Drop tables if they are present
DROP TABLE IF EXISTS DeliveryDetails;
DROP TABLE IF EXISTS Delivery;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS WineDistribution;
DROP TABLE IF EXISTS Distributor;
DROP TABLE IF EXISTS WineProduction;
DROP TABLE IF EXISTS SuppliedComponents;
DROP TABLE IF EXISTS SupplyOrder;
DROP TABLE IF EXISTS Supplier;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS SalesReport;
DROP TABLE IF EXISTS Wine;
DROP TABLE IF EXISTS GrapeHarvest;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Department;

SET FOREIGN_KEY_CHECKS = 1;
-- Employee Table
CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    DepartmentID INT NOT NULL,
    WorkWeekHours INT NOT NULL,
    WeekNumber INT NOT NULL,
    Position VARCHAR(100) NOT NULL
);

-- Department Table
CREATE TABLE Department (
    DepartmentID INT PRIMARY KEY AUTO_INCREMENT,
    WeekNumber INT NOT NULL,
    ManagerName VARCHAR(100) NOT NULL,
    Name VARCHAR(100) NOT NULL
);
-- Wine Table
CREATE TABLE Wine (
    WineID INT PRIMARY KEY AUTO_INCREMENT,
    WineName VARCHAR(255) NOT NULL,
    WineType VARCHAR(100) NOT NULL,
    InventoryQuantity DECIMAL(10,2) NOT NULL DEFAULT 0,
    SalesVolume INT DEFAULT 0
);

-- Grape Harvest Table
CREATE TABLE GrapeHarvest (
    HarvestID INT PRIMARY KEY AUTO_INCREMENT,
    GrapeType VARCHAR(50) NOT NULL,
    HarvestDate DATE NOT NULL,
    YieldQuantity DECIMAL(10,2) NOT NULL,
    QualityRating INT CHECK (QualityRating BETWEEN 1 AND 10)
);

-- Supplier Table
CREATE TABLE Supplier (
    SupplierID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    ComponentType VARCHAR(100) NOT NULL,
    ContactInfo VARCHAR(255) NOT NULL
);

-- Supply Order Table
CREATE TABLE SupplyOrder (
    SupplyOrderID INT PRIMARY KEY AUTO_INCREMENT,
    SupplierID INT NOT NULL,
    OrderDate DATE NOT NULL,
    ExpectedDelivery DATE NOT NULL,
    ActualDelivery DATE,
    Status ENUM('Pending', 'Delivered', 'Late', 'Shipped') NOT NULL,
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

-- Supplied Components Table
CREATE TABLE SuppliedComponents (
    SupplyID INT PRIMARY KEY AUTO_INCREMENT,
    SupplyOrderID INT NOT NULL,
    SupplierID INT NOT NULL,
    ComponentName VARCHAR(100) NOT NULL,
    QuantitySupplied INT NOT NULL,
    DateSupplied DATE NOT NULL,
    FOREIGN KEY (SupplyOrderID) REFERENCES SupplyOrder(SupplyOrderID),
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

-- Wine Production Table
CREATE TABLE WineProduction (
    ProductionID INT PRIMARY KEY AUTO_INCREMENT,
    HarvestID INT NOT NULL,
    WineID INT NOT NULL,
    QuantityProduced DECIMAL(10,2) NOT NULL,
    ProductionDate DATE NOT NULL,
    FOREIGN KEY (HarvestID) REFERENCES GrapeHarvest(HarvestID),
    FOREIGN KEY (WineID) REFERENCES Wine(WineID)
);

-- Distributor Table
CREATE TABLE Distributor (
    DistributorID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    ContactInfo VARCHAR(255) NOT NULL,
    Region VARCHAR(100) NOT NULL
);

-- Wine Distribution Table
CREATE TABLE WineDistribution (
    DistributionID INT PRIMARY KEY AUTO_INCREMENT,
    WineID INT NOT NULL,
    DistributorID INT NOT NULL,
    DateShipped DATE NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (WineID) REFERENCES Wine(WineID),
    FOREIGN KEY (DistributorID) REFERENCES Distributor(DistributorID)
);

-- Order Table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    DistributorID INT NOT NULL,
    OrderDate DATE NOT NULL,
    ShipDate DATE,
    Status ENUM('Pending', 'Shipped', 'Completed') NOT NULL,
    FOREIGN KEY (DistributorID) REFERENCES Distributor(DistributorID)
);

-- Delivery Table
CREATE TABLE Delivery (
    DeliveryID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT NOT NULL,
    Status ENUM('Pending', 'Delivered', 'Late', 'Shipped', 'Completed') NOT NULL,
    ExpectedDate DATE NOT NULL,
    ActualDate DATE,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

-- Delivery Details Table
CREATE TABLE DeliveryDetails (
    DeliveryDetailID INT PRIMARY KEY AUTO_INCREMENT,
    DeliveryID INT NOT NULL,
    OrderID INT NOT NULL,
    QuantityShipped INT NOT NULL,
    FOREIGN KEY (DeliveryID) REFERENCES Delivery(DeliveryID),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

-- Sales Report Table
CREATE TABLE SalesReport (
    ReportID INT PRIMARY KEY AUTO_INCREMENT,
    WineID INT NOT NULL,
    SalesVolume INT NOT NULL,
    Date DATE NOT NULL,
    FOREIGN KEY (WineID) REFERENCES Wine(WineID)
);

-- Inventory Table
CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY AUTO_INCREMENT,
    WineID INT NOT NULL,
    SupplyID INT NOT NULL,
    QuantityInStock INT NOT NULL DEFAULT 0,
    FOREIGN KEY (WineID) REFERENCES Wine(WineID),
    FOREIGN KEY (SupplyID) REFERENCES SuppliedComponents(SupplyID)
);
-- Department 
INSERT INTO Department (WeekNumber, ManagerName, Name) VALUES 
(8, 'Janet Collins', 'Finance'),
(8, 'Roz Murphy', 'Marketing'),
(8, 'Henry Doyle', 'Production'),
(8, 'Maria Costanza', 'Distribution');

-- Employee 
INSERT INTO Employee (Name, DepartmentID, WorkWeekHours, WeekNumber, Position) VALUES 
('Janet Collins', 1, 40, 8, 'Payroll Manager'),
('Roz Murphy', 2, 36.5, 8, 'Head of Marketing'),
('Bob Ulrich', 2, 50, 8, 'Marketing Assistant'),
('Henry Doyle', 3, 40, 8, 'Production Manager'),
('Maria Costanza', 4, 40, 8, 'Logistics Manager'),
('John Smith', 3, 40, 8, 'Vineyard Supervisor');

INSERT INTO Wine (WineName, WineType, SalesVolume) VALUES
('Merlot Reserve', 'Red', 500),
('Cabernet Estate', 'Red', 450),
('Chablis Premium', 'White', 350),
('Chardonnay Classic', 'White', 400);

-- Grape Harvest 
INSERT INTO GrapeHarvest (GrapeType, HarvestDate, YieldQuantity, QualityRating) VALUES 
('Cabernet', '2024-09-01', 1500.50, 9),
('Chardonnay', '2024-09-05', 1300.75, 8),
('Merlot', '2024-09-10', 1100.20, 7),
('Chablis', '2024-09-15', 1200.65, 8),
('Merlot', '2024-09-20', 1400.30, 9),
('Chardonnay', '2024-09-25', 1250.80, 8);

-- Supplier 
INSERT INTO Supplier (Name, ComponentType, ContactInfo) VALUES 
('Supplier A', 'Bottles and Corks', 'contactA@example.com'),
('Supplier B', 'Labels and Boxes', 'contactB@example.com'),
('Supplier C', 'Vats and Tubing', 'contactC@example.com');

-- Distributor 
INSERT INTO Distributor (Name, ContactInfo, Region) VALUES 
('Distributor One', 'one@example.com', 'North'),
('Distributor Two', 'two@example.com', 'South'),
('Distributor Three', 'three@example.com', 'East'),
('Distributor Four', 'four@example.com', 'West'),
('Distributor Five', 'five@example.com', 'Midwest'),
('Distributor Six', 'six@example.com', 'International');

-- Orders 
INSERT INTO Orders (DistributorID, OrderDate, ShipDate, Status) VALUES 
(1, '2024-10-01', NULL, 'Pending'),
(2, '2024-10-02', NULL, 'Pending'),
(3, '2024-10-03', '2024-10-07', 'Shipped'),
(4, '2024-10-04', '2024-10-08', 'Shipped'),
(5, '2024-10-05', '2024-10-09', 'Completed'),
(6, '2024-10-06', '2024-10-10', 'Completed');


-- Wine Table
INSERT INTO Wine (WineName, WineType, InventoryQuantity, SalesVolume) VALUES 
('Merlot Reserve', 'Red', 0.00, 500),
('Cabernet Estate', 'Red', 0.00, 450),
('Chablis Premium', 'White', 0.00, 350),
('Chardonnay Classic', 'White', 0.00, 400);



-- Supply Order 
INSERT INTO SupplyOrder (SupplierID, OrderDate, ExpectedDelivery, ActualDelivery, Status) VALUES
(1, '2024-09-01', '2024-09-10', '2024-09-09', 'Delivered'),
(2, '2024-09-05', '2024-09-12', '2024-09-12', 'Pending'),  
(3, '2024-09-07', '2024-09-14', '2024-09-13', 'Shipped'),
(1, '2024-09-02', '2024-09-12', '2024-09-12', 'Delivered'),
(1, '2024-09-04', '2024-09-16', '2024-09-15', 'Delivered'),
(3, '2024-09-06', '2024-09-20', '2024-09-19', 'Delivered');

-- Supplied Components 
INSERT INTO SuppliedComponents (SupplyOrderID, SupplierID, ComponentName, QuantitySupplied, DateSupplied) VALUES 
(1, 1, 'Corks', 5000, '2024-09-09'),
(2, 2, 'Labels', 4500, '2024-09-12'),
(3, 3, 'Vats', 10, '2024-09-14'),
(4, 1, 'Bottles', 6000, '2024-09-15'),
(5, 2, 'Boxes', 500, '2024-09-17'),
(6, 3, 'Tubing', 15, '2024-09-19');

-- Wine Distribution 
INSERT INTO WineDistribution (WineID, DistributorID, DateShipped, Quantity) VALUES 
(1, 1, '2024-10-07', 250),
(2, 2, '2024-10-08', 200),
(3, 3, '2024-10-09', 180),
(4, 4, '2024-10-10', 150),
(1, 5, '2024-10-11', 300),
(2, 6, '2024-10-12', 275);

-- Delivery 
INSERT INTO Delivery (OrderID, Status, ExpectedDate, ActualDate) VALUES 
(1, 'Pending', '2024-10-14', NULL),
(2, 'Pending', '2024-10-15', NULL),
(3, 'Shipped', '2024-10-16', '2024-10-15'),
(4, 'Shipped', '2024-10-17', '2024-10-16'),
(5, 'Completed', '2024-10-18', '2024-10-18'),
(6, 'Completed', '2024-10-19', '2024-10-19');

-- Delivery Details 
INSERT INTO DeliveryDetails (DeliveryID, OrderID, QuantityShipped) VALUES 
(1, 1, 250),
(2, 2, 200),
(3, 3, 180),
(4, 4, 150),
(5, 5, 300),
(6, 6, 275);

-- Sales Report 
INSERT INTO SalesReport (WineID, SalesVolume, Date) VALUES 
(1, 500, '2024-10-15'),
(2, 400, '2024-10-16'),
(3, 350, '2024-10-17'),
(4, 250, '2024-10-18'),
(1, 550, '2024-10-19'),
(2, 450, '2024-10-20');

-- Inventory 
INSERT INTO Inventory (WineID, SupplyID, QuantityInStock) VALUES 
(1, 1, 1000),
(2, 2, 800),
(3, 3, 750),
(4, 4, 600),
(1, 5, 1200),
(2, 6, 950);

-- Wine Production Table
INSERT INTO wineproduction (HarvestID, WineID, QuantityProduced, ProductionDate) VALUES
(1, 1, 1000, '2024-10-01'),
(2, 2, 900, '2024-10-02'),
(3, 3, 850, '2024-10-03'),
(4, 4, 700, '2024-10-04'),
(5, 1, 1100, '2024-10-05'),
(6, 2, 1050, '2024-10-06');

