'use client';

interface OrderStatusStepperProps {
  status: string;
}

const statuses = [
  { key: 'pending', label: 'Order Placed' },
  { key: 'confirmed', label: 'Confirmed' },
  { key: 'preparing', label: 'Preparing' },
  { key: 'out_for_delivery', label: 'Out for Delivery' },
  { key: 'delivered', label: 'Delivered' },
];

export default function OrderStatusStepper({ status }: OrderStatusStepperProps) {
  const currentIndex = statuses.findIndex((s) => s.key === status);

  return (
    <div className="w-full">
      {/* Desktop - Horizontal */}
      <div className="hidden md:flex items-center justify-between">
        {statuses.map((step, index) => {
          const isCompleted = index <= currentIndex;
          const isCurrent = index === currentIndex;

          return (
            <div key={step.key} className="flex items-center flex-1">
              <div className="flex flex-col items-center flex-1">
                <div
                  className={`w-12 h-12 rounded-full flex items-center justify-center border-4 transition-all ${
                    isCompleted
                      ? 'bg-primary border-primary'
                      : 'bg-gray-200 border-gray-300'
                  } ${isCurrent ? 'animate-pulse' : ''}`}
                >
                  {isCompleted ? (
                    <svg
                      className="w-6 h-6 text-white"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                  ) : (
                    <span className="text-gray-500 font-semibold">{index + 1}</span>
                  )}
                </div>
                <span
                  className={`mt-2 text-sm font-medium ${
                    isCompleted ? 'text-primary' : 'text-gray-500'
                  }`}
                >
                  {step.label}
                </span>
              </div>
              {index < statuses.length - 1 && (
                <div
                  className={`h-1 flex-1 mx-2 ${
                    index < currentIndex ? 'bg-primary' : 'bg-gray-300'
                  }`}
                />
              )}
            </div>
          );
        })}
      </div>

      {/* Mobile - Vertical */}
      <div className="md:hidden space-y-4">
        {statuses.map((step, index) => {
          const isCompleted = index <= currentIndex;
          const isCurrent = index === currentIndex;

          return (
            <div key={step.key} className="flex items-start gap-4">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center border-4 flex-shrink-0 transition-all ${
                  isCompleted
                    ? 'bg-primary border-primary'
                    : 'bg-gray-200 border-gray-300'
                } ${isCurrent ? 'animate-pulse' : ''}`}
              >
                {isCompleted ? (
                  <svg
                    className="w-5 h-5 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                ) : (
                  <span className="text-gray-500 font-semibold text-sm">
                    {index + 1}
                  </span>
                )}
              </div>
              <div className="flex-1 pt-1">
                <span
                  className={`text-sm font-medium ${
                    isCompleted ? 'text-primary' : 'text-gray-500'
                  }`}
                >
                  {step.label}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
