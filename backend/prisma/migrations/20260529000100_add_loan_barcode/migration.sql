-- Add barcode to Loan so migrations match the current Prisma schema and seed data.
-- Existing rows are assigned deterministic unique values based on their id.

PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;

CREATE TABLE "new_Loan" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "copyId" INTEGER NOT NULL,
    "userId" INTEGER NOT NULL,
    "barcode" TEXT NOT NULL,
    "checkoutDate" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "dueDate" DATETIME NOT NULL,
    "returnDate" DATETIME,
    "fineAmount" REAL NOT NULL DEFAULT 0,
    "finePaid" BOOLEAN NOT NULL DEFAULT false,
    "fineForgiven" BOOLEAN NOT NULL DEFAULT false,
    "renewCount" INTEGER NOT NULL DEFAULT 0,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "Loan_copyId_fkey" FOREIGN KEY ("copyId") REFERENCES "Copy" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "Loan_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

INSERT INTO "new_Loan" (
    "id",
    "copyId",
    "userId",
    "barcode",
    "checkoutDate",
    "dueDate",
    "returnDate",
    "fineAmount",
    "finePaid",
    "fineForgiven",
    "renewCount",
    "createdAt",
    "updatedAt"
)
SELECT
    "id",
    "copyId",
    "userId",
    'LN-MIGRATED-' || "id",
    "checkoutDate",
    "dueDate",
    "returnDate",
    "fineAmount",
    "finePaid",
    "fineForgiven",
    "renewCount",
    "createdAt",
    "updatedAt"
FROM "Loan";

DROP TABLE "Loan";
ALTER TABLE "new_Loan" RENAME TO "Loan";

CREATE UNIQUE INDEX "Loan_barcode_key" ON "Loan"("barcode");

PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;
